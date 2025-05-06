# -*- coding: utf-8 -*-

import base64
import logging
import unicodedata
import math, random
from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError, UserError
from odoo.addons.portal.controllers.portal import CustomerPortal

_logger = logging.getLogger(__name__)

class CalendarController(http.Controller):

	@http.route('/calendar_event/attendance_manual_entery', type='json', auth='public', csrf=False)
	def calendar_event_attendance_manual_entery(self,**kw):
		if kw.get('calendar_id'):
			calendar_id = request.env['calendar.event'].browse(kw.get('calendar_id'))
			calendar_id.attendance_manual_entery(kw.get('partner_id'),kw.get('type'))

	@http.route('/calendar_event/log_outgoing_message', type='json', auth='public', csrf=False)
	def calendar_event_log_outgoing_message(self,**kw):
		if kw.get('calendar_id'):
			calendar_id = request.env['calendar.event'].browse(kw.get('calendar_id'))
			calendar_id.log_outgoing_message(kw.get('message'))

	@http.route('/meeting/<int:calendar_event>', type='http', auth='user', website=True)
	def channel_rating(self, calendar_event, **kw):
		values = {}
		server_url = request.env['ir.config_parameter'].sudo().get_param('jitsi.server', default='https://meet.jit.si/')
		jitsi_meet_domain = request.env['ir.config_parameter'].sudo().get_param('jitsi.server.domain',
																				default='meet.jit.si')
		partner_id = request.env.user.partner_id
		# calendar_event = request.env['calendar.event'].sudo().browse(calendar_event)
		calendar_event = request.env['calendar.event'].sudo().browse(calendar_event)
		login_partner_exist = calendar_event.partner_ids.filtered(lambda l: l.id == partner_id.id)
		if not login_partner_exist and calendar_event.anonymous_participant:
			calendar_event.partner_ids = [(4, partner_id.id)]
			calendar_event.anonymous_partner_ids = [(4, partner_id.id)]
			calendar_event.anonymous_user_ids = [(4, request.env.user.id)]
		elif not login_partner_exist and not calendar_event.anonymous_participant:
			# if calendar_event.partner_ids.mapped('name') not in request.env.user.name:
			values.update({'errors': 'You are not access this Session Please Ask To Administrator'})
		if not values.get('errors'):
			attachments = False
			if calendar_event.document_list_preview:
				attachments = request.env["ir.attachment"].sudo().search(
					[('res_model', '=', 'calendar.event'), ('res_id', '=', calendar_event.id)])
			partner_ids = []
			for partner in calendar_event.partner_ids:
				last_partner_history = request.env['participant.history'].sudo().search(
					[('calendar_event_id', '=', calendar_event.id), ('partner_id', '=', partner.id)], limit=1)
				attendance_state = last_partner_history.attendance_state
				partner_ids.append({'partner_id': partner, 'attendance_state': attendance_state})
			values.update({'attachments': attachments,
						   'partner_ids': partner_ids})

		attendance_state = calendar_event.get_login_user_attendance_state()

		values.update({'calendar_event': calendar_event,
					   'server_url': server_url,
					   'jitsi_meet_domain': jitsi_meet_domain,
					   'current_user': request.env.user,
					   'partner_id': partner_id,
					   'attendance_state': attendance_state,
					   })
		return request.render("do_video_conference.page_meeting_template", values)

	@http.route('/meeting/attachment/add', type='json', auth='public', methods=['POST'], website=True, csrf=False)
	def attachment_add(self,access_token=None, **kwargs):
		name = kwargs.get("name")
		file = kwargs.get("file")
		res_model = kwargs.get("res_model")
		res_id = kwargs.get("res_id")
		try:
			CustomerPortal._document_check_access(self, res_model, int(res_id), access_token=access_token)
		except (AccessError, MissingError) as e:
			_logger.info("Error To access Document: %s" % e)
			raise UserError(_("The document does not exist or you do not have the rights to access it."))

		IrAttachment = request.env['ir.attachment'].sudo()
		access_token = False

		# Avoid using sudo or creating access_token when not necessary: internal
		# users can create attachments, as opposed to public and portal users.
		if not request.env.user.has_group('base.group_user'):
			IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)
			access_token = IrAttachment._generate_access_token()

		# At this point the related message does not exist yet, so we assign
		# those specific res_model and res_is. They will be correctly set
		# when the message is created: see `portal_chatter_post`,
		# or garbage collected otherwise: see  `_garbage_collect_attachments`.
		values = {
			'name': name,
			'res_model': res_model,
			'res_id': int(res_id),
			'access_token': access_token,
		}
		if file and kwargs.get('type') == 'binary':
			filename = kwargs.get("filename")
			files_list = file.split(',')
			file_str = files_list[-1] if files_list else ""
			binary_data = base64.b64decode(file_str)
			base64_encoded_data = base64.b64encode(binary_data).decode('utf-8')			
			# values.update({'datas': base64.b64encode(file.read()),'type': 'binary'})
			values.update({'datas': base64_encoded_data,'type': 'binary'})
			if request.httprequest.user_agent.browser == 'safari':
				# Safari sends NFD UTF-8 (where é is composed by 'e' and [accent])
				# we need to send it the same stuff, otherwise it'll fail
				filename = unicodedata.normalize('NFD', filename)
			values.update({'name': filename})
		if kwargs.get('type') == 'url':
			values.update({'url': kwargs.get('url'),'type': 'url'})
		attachment = IrAttachment.create(values)
		_logger.info("Attachment Id: %s" % attachment)
		# attachment.cron_synchronize_attachments()
		attachments = IrAttachment.search([('res_model', '=', 'calendar.event'), ('res_id', '=', int(res_id))])
		calendar_id = request.env['calendar.event'].sudo().browse(int(res_id))
		calendar_id.create_attachment_history_line(request.env.user.partner_id.id, 'upload', attachment.id)
		response_content = request.env['ir.ui.view']._render_template('do_video_conference.website_ir_attachment_list',{'attachments': attachments,'calendar_event': calendar_id.sudo()})
		calendar_id._notify_channel()

		# response_return = request.make_response(
		# 	data=response_content,
		# 	headers=[('Content-Type', 'text/html; charset=utf-8')]
		# )

		return {'response_content':response_content}

	@http.route('/meeting/attachment/delete', type='json', auth='public')
	def attachment_delete(self, res_id, attachment_id, **kwargs):
		values = {}
		if res_id and attachment_id:
			IrAttachment = request.env['ir.attachment'].sudo()
			calendar_id = request.env['calendar.event'].sudo().browse(int(res_id))
			calendar_id.create_attachment_history_line(request.env.user.partner_id.id, 'delete', attachment_id)
			IrAttachment.search([('id', '=', int(attachment_id))], limit=1).unlink()
			attachments = IrAttachment.search([('res_model', '=', 'calendar.event'), ('res_id', '=', int(res_id))])
			response_content = request.env['ir.ui.view']._render_template(
				'do_video_conference.website_ir_attachment_list',
				{'attachments': attachments, 'calendar_event': calendar_id.sudo()})
			calendar_id._notify_channel()
			values.update({'response_content': response_content})
		return values

	@http.route('/meeting/attachment/fetch', type='json', auth='public')
	def attachment_fetch(self, res_id, **kwargs):
		values = {}
		if res_id:
			IrAttachment = request.env['ir.attachment'].sudo()
			attachments = IrAttachment.search([('res_model', '=', 'calendar.event'), ('res_id', '=', int(res_id))])
			calendar_id = request.env['calendar.event'].sudo().browse(int(res_id))
			response_content = request.env['ir.ui.view']._render_template(
				'do_video_conference.website_ir_attachment_list',
				{'attachments': attachments, 'calendar_event': calendar_id.sudo()})
			values.update({'do_video_conference.website_ir_attachment_list': response_content})
		return values

	@http.route('/meeting/attachment/log', type='json', auth='public')
	def attachment_logo(self, res_id, attachment_id, type, **kwargs):
		values = {}
		if res_id and attachment_id:
			calendar_id = request.env['calendar.event'].sudo().browse(int(res_id))
			partner_id = request.env.user.partner_id
			calendar_id.create_attachment_history_line(partner_id.id, type, attachment_id)
		return values

	@http.route('/meeting/get_participant_status', type='json', auth='public')
	def get_participant_status(self, res_id, **kwargs):
		values = {}
		if res_id:
			calendar_id = request.env['calendar.event'].sudo().browse(int(res_id))
			partner_ids = []
			for partner_id in calendar_id.partner_ids:
				last_partner_history = request.env['participant.history'].sudo().search(
					[('calendar_event_id', '=', calendar_id.id), ('partner_id', '=', partner_id.id)], limit=1)
				attendance_state = last_partner_history.attendance_state
				partner_ids.append({'partner_id': partner_id, 'attendance_state': attendance_state})

			response_content = request.env['ir.ui.view']._render_template(
				'do_video_conference.participant_status_template',
				{'calendar_event': calendar_id, 'partner_ids': partner_ids})
			values.update({'do_video_conference.participant_status_template': response_content})
		return values

	@http.route('/meeting/note/add', type='json', auth='public')
	def meeting_note_add(self, res_id, user_id, value, **kwargs):
		if res_id and user_id and value:
			calendar_id = request.env['calendar.event'].sudo().browse(int(res_id))
			notes_id = request.env['project.task'].sudo().search([('calendar_event_id', '=', calendar_id.id)], limit=1)
			notes_id = notes_id.filtered(lambda x:user_id in x.user_ids.ids)
			if notes_id:
				notes_id.write({'description': value})
			else:
				request.env['project.task'].sudo().create({'calendar_event_id': calendar_id.id,'description': value,'user_ids': [int(user_id)]})
		return {}

	# function to generate OTPS
	def generateOTP(self):

		# Declare a string variable
		# which stores all string
		string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
		OTP = ""
		length = len(string)
		for i in range(8):
			OTP += string[math.floor(random.random() * length)]
		return OTP

	@http.route('/meeting/send_otp', type='json', auth='public')
	def meeting_send_otp(self, res_id, **kwargs):
		if request.env.user and request.env.user.partner_id and res_id:
			calendar_id = request.env['calendar.event'].sudo().browse(int(res_id))
			if calendar_id and calendar_id.is_otp_enable:
				otp = self.generateOTP()
				request.env.user.partner_id.meeting_otp = otp
				if calendar_id.otp_type_email:
					template = request.env.ref('do_video_conference.meeting_otp_mail_template',
											   raise_if_not_found=False)
					if template:
						template.sudo().send_mail(request.env.user.partner_id.id, force_send=True)
		return {}

	@http.route('/meeting/verify_otp', type='json', auth='public')
	def meeting_verify_otp(self, res_id, **kwargs):
		error = False
		otp = kwargs.get('otp')
		if request.env.user and request.env.user.partner_id and otp:
			if request.env.user.partner_id.meeting_otp != otp:
				error = _('OTP is not Valid.')
		else:
			error = _('Please insert OTP')
		return {'error': error}

	@http.route('/meeting/bbb_password_check', type='json', auth='public')
	def bbb_meeting_verify_password(self, res_id, password, **kwargs):
		error = False
		if request.env.user and request.env.user.partner_id and res_id and password:
			calendar_id = request.env['calendar.event'].sudo().browse(int(res_id))
			if calendar_id.bbb_attendeePW == password:
				bbb_join_url = calendar_id.join_bigbluebutton_meeting(password)
				return {'error': error,
						'bbb_attendee': True,
						'bbb_join_url': bbb_join_url}
			if calendar_id.bbb_moderatorPW == password:
				bbb_join_url = calendar_id.join_bigbluebutton_meeting(password)
				return {'error': error,
						'bbb_moderator': True,
						'bbb_join_url': bbb_join_url}
			else:
				error = _('Password is not Valid.')
		else:
			error = _('Please insert password')
		return {'error': error}
