# -*- coding: utf-8 -*-

import json
from random import choice
from odoo import api, fields, models, _
from bigbluebutton_api_python import BigBlueButton
from bigbluebutton_api_python.parameters.bbbmodule import BBBModule
from odoo.exceptions import UserError, ValidationError
import pytz
from odoo.http import request
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

#
# def create_hash():
#     size = 32
#     values = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
#     p = ''
#     p = p.join([choice(values) for i in range(size)])
#     return p

class MeetingParticipantHistory(models.Model):
	_name = "participant.history"
	_description = "Participant History"
	_order = "join_datetime desc"

	name = fields.Char(string='Participant name')
	jitsi_id = fields.Char(string='JITSI ID')
	partner_id = fields.Many2one('res.partner', string='Partner', compute="_compute_partner_id", inverse="_inverse_partner_id", store=True, required=True)
	join_datetime = fields.Datetime(string='Join Date time')
	left_datetime = fields.Datetime(string='Left Date time')
	calendar_event_id = fields.Many2one('calendar.event', 'Session', required=True)
	attendance_state = fields.Selection(string="Attendance Status", selection=[('checked_out', "Checked out"), ('checked_in', "Checked in")])

	@api.depends('name')
	def _compute_partner_id(self):
		self.partner_id = self.env['res.partner']
		for record in self:
			if record.name:
				partner_id = self.env['res.partner'].sudo().search([('name', 'ilike', record.name)], limit=1)
				if partner_id:
					record.partner_id = partner_id.id

	def _inverse_partner_id(self):
		for record in self:
			if record.partner_id:
				record.name = record.partner_id.name

	@api.model_create_multi
	def create(self, values):
		participant_history_id = super(MeetingParticipantHistory, self).create(values)
		if participant_history_id and participant_history_id.partner_id and participant_history_id.calendar_event_id:
			HistoryTotalTime = self.env['participant.history.total.time'].sudo()
			history_total_time_id = HistoryTotalTime.search([('partner_id', '=', participant_history_id.partner_id.id),
															 ('calendar_event_id', '=', participant_history_id.calendar_event_id.id)], limit=1)
			if not history_total_time_id:
				HistoryTotalTime.create({'calendar_event_id': participant_history_id.calendar_event_id.id,
										 'partner_id': participant_history_id.partner_id.id})
		return participant_history_id

	def write(self, vals):
		res = super(MeetingParticipantHistory, self).write(vals)
		return res

class MeetingParticipantHistoryTotalTime(models.Model):
	_name = "participant.history.total.time"
	_description = "Participant Total Time"
	_rec_name = 'partner_id'

	calendar_event_id = fields.Many2one('calendar.event', 'Session', required=True)
	partner_id = fields.Many2one('res.partner', string='Partner', required=True)
	total_time = fields.Float(compute="compute_total_time", string="Total Time (Minute's)")

	@api.depends('calendar_event_id', 'calendar_event_id.participant_history_ids')
	def compute_total_time(self):
		for record in self:
			total_time = 0.0
			if record.calendar_event_id and record.calendar_event_id.participant_history_ids:
				for history_id in record.calendar_event_id.participant_history_ids:
					if history_id.partner_id.id == record.partner_id.id:
						if history_id.join_datetime and history_id.left_datetime:
							time_delta = (history_id.left_datetime - history_id.join_datetime)
						elif history_id.join_datetime and not history_id.left_datetime:
							time_delta = (fields.Datetime.now() - history_id.join_datetime)
						total_seconds = time_delta.total_seconds()
						minutes = total_seconds/60
						total_time += minutes
			record.total_time = total_time

class Task(models.Model):
	_inherit = 'project.task'

	calendar_event_id = fields.Many2one('calendar.event', 'Session')

class MeetingAttachmentHistory(models.Model):
	_name = "meeting.attachment.history"
	_description = "Session Attachment History"
	_order = "action_date desc"

	name = fields.Char(string='Participant name')
	partner_id = fields.Many2one('res.partner', string='Partner', compute="_compute_partner_id", inverse="_inverse_partner_id", store=True)
	type = fields.Selection([('download', 'Download'), ('preview', 'Perview'), ('upload', 'Upload'), ('delete', 'Delete')], string="Type")
	action_date = fields.Datetime(string='Action Date time')
	attachment_id = fields.Many2one('ir.attachment', string='Attachment')
	calendar_event_id = fields.Many2one('calendar.event', 'Session')

	@api.depends('name')
	def _compute_partner_id(self):
		self.partner_id = self.env['res.partner']
		for record in self:
			if record.name:
				partner_id = self.env['res.partner'].sudo().search([('name', 'ilike', record.name)], limit=1)
				if partner_id:
					record.partner_id = partner_id.id

	def _inverse_partner_id(self):
		for record in self:
			if record.partner_id:
				record.name = record.partner_id.name

class Meeting(models.Model):
	_inherit = 'calendar.event'

	anonymous_participant = fields.Boolean(string='Anonymous Participant')
	conference_type = fields.Selection([('jitsi', 'JITSI'), ('bigbluebutton', 'Big Blue Button')], string="Video Conference Type", default="jitsi")
	video_conference = fields.Boolean('Video Conference', default=True)
	jitsi_password = fields.Char(string='Password')
	hash = fields.Char('Hash', copy=False)
	url = fields.Char(string='URL to Session', compute='_compute_url')
	closed = fields.Boolean('Closed', default=False)
	document_list_preview = fields.Boolean('Document list and preview', default=True)
	document_list_preview_user_ids = fields.Many2many('res.users', 'document_list_preview_user_rel', 'event_id', 'user_id', string='Document Upload Permission')
	document_delete = fields.Boolean(string='Document Delete')
	document_delete_ids = fields.Many2many('res.users', 'document_delete_user_rel', 'event_id', 'user_id', string='Document Delete Users')
	chat_jitsi = fields.Boolean('JITSI Chat', default=True)
	notify_event_channel_name = fields.Char(compute="_compute_channel_names")
	participant_history_ids = fields.One2many('participant.history', 'calendar_event_id', string='Participant History')
	anonymous_user_ids = fields.Many2many('res.users', 'anonymous_event_user_rel', 'event_id', 'user_id', string='Anonymous Users')
	anonymous_partner_ids = fields.Many2many('res.partner', 'anonymous_event_partner_rel', 'event_id', 'partner_id', string="Anonymous Partner")
	notes_ids = fields.One2many('project.task', 'calendar_event_id', string='Notes')
	bbb_meeting_id = fields.Char(string='BigBlueButton Session ID')
	bbb_attendeePW = fields.Char(string='BigBlueButton Attendee Password')
	bbb_moderatorPW = fields.Char(string='BigBlueButton Moderator Password')
	bbb_allow_to_record_meeting = fields.Boolean(string='Allow to Recording Session')
	bbb_allow_start_stop_recording = fields.Boolean(string='Allow Start and Stop Recording')
	bbb_auto_start_recording = fields.Boolean(string='Auto Start Recording')
	bbb_mute_on_start = fields.Boolean(string='Mute on Start')
	bbb_default_presentation = fields.Binary(string='Default Presentation', attachment=True)
	bbb_default_presentation_name = fields.Char(string='Default Presentation Name')
	attachment_history_ids = fields.One2many('meeting.attachment.history', 'calendar_event_id', string='Attachment History')
	is_otp_enable = fields.Boolean(string='OTP Enable')
	otp_type_email = fields.Boolean(string='Email OTP')
	participant_history_group_ids = fields.One2many('participant.history.total.time', 'calendar_event_id', string='Participant Group')

	def attachment_add(self):
		print('------------call')

	def get_date_format(self,date_field):
		utc_datetime = datetime.strptime(date_field, "%Y-%m-%d %H:%M:%S")
		utc_timezone = pytz.utc
		utc_datetime = utc_timezone.localize(utc_datetime)
		local_timezone = pytz.timezone(request.env.user.tz)
		local_datetime = utc_datetime.astimezone(local_timezone)
		local_datetime_str = local_datetime.strftime("%Y-%m-%dT%H:%M")
		return local_datetime_str

	def action_open_users(self):
		self.ensure_one()
		if self.partner_ids:
			users_ids = self.env['res.users'].sudo().search([('partner_id', 'in', self.partner_ids.ids)])
			action = self.env.ref('base.action_res_users').read()[0]
			action['domain'] = [('id', 'in', users_ids.ids)]
			action['context'] = {}
			return action

	def action_open_participant_history(self):
		self.ensure_one()
		if self.participant_history_ids:
			action = self.env.ref('do_video_conference.participant_history_action').read()[0]
			action['domain'] = [('id', 'in', self.participant_history_ids.ids)]
			action['context'] = {}
			return action

	def action_open_participant_history_group(self):
		self.ensure_one()
		if self.participant_history_group_ids:
			action = self.env.ref('do_video_conference.participant_history_group_action').read()[0]
			action['domain'] = [('id', 'in', self.participant_history_group_ids.ids)]
			action['context'] = {}
			return action

	@api.depends("create_date")
	def _compute_channel_names(self):
		for record in self:
			res_id = record.id
			record.notify_event_channel_name = "notify_event_%s" % res_id

	_sql_constraints = [
		('metting_name_uniq', 'unique (name)', 'Metting name already exists!'),
	]

	def action_close_meeting(self):
		self.write({'closed': True})

	def action_reopen_meeting(self):
		self.write({'closed': False})

	@api.model_create_multi
	def create(self, vals):
		res = super(Meeting, self).create(vals)
		return res

	@api.model
	def _compute_url(self):
		for r in self:
			url = '%s/meeting/%s' % (self.env['ir.config_parameter'].sudo().get_param('web.base.url'), r.id)
			r.url = url

	def open(self):
		url = '/meeting/' + str(self.id)
		return {'name': 'Session',
				'res_model': 'ir.actions.act_url',
				'type': 'ir.actions.act_url',
				'target': 'new',
				'url': url
				}

	def _notify_channel(self, title=None, sticky=False):
		channel_name_field = self.notify_event_channel_name
		bus_message = {
			"type": "attachment_added",
			"message": _('Attachment ADD'),
			"title": title,
			"sticky": sticky,
		}
		notifications = [
			(channel_name_field, 'mail.channel/new_message', bus_message) for record in self
		]
		# self.env["bus.bus"]._sendmany(notifications)

	def _notify_channel_attendance(self, title=None, sticky=False):
		channel_name_field = self.notify_event_channel_name
		bus_message = {
			"type": "attendance_manual_entery",
			"message": _('Attendance Manual Entery'),
			"title": title,
			"sticky": sticky,
		}
		notifications = [
			(channel_name_field, 'mail.channel/new_message', bus_message) for record in self
		]
		# self.env["bus.bus"]._sendmany(notifications)

	def attendance_manual(self, jitsi_id, name=None):
		self.ensure_one()
		action_date = fields.Datetime.now()
		ParticipantHistory = self.env['participant.history'].sudo()
		participant_history_id = False
		if jitsi_id:
			participant_history_id = ParticipantHistory.search([('jitsi_id', '=', jitsi_id), ('calendar_event_id', '=', self.id)], limit=1)
			if participant_history_id and not name:
				participant_history_id.write({'left_datetime': action_date,
											  'attendance_state': 'checked_out'})
			elif not participant_history_id:
				participant_history_id = ParticipantHistory.create({'name': name,
																	'jitsi_id': jitsi_id,
																	'join_datetime': action_date,
																	'attendance_state': 'checked_in',
																	'calendar_event_id': self.id})
		return participant_history_id

	def attendance_manual_entery(self, partner_id, attendance_state):
		self.ensure_one()
		action_date = fields.Datetime.now()
		ParticipantHistory = self.env['participant.history'].sudo()
		participant_history_id = False
		if partner_id:
			partner_id = self.env['res.partner'].sudo().browse(int(partner_id))
			participant_history_id = ParticipantHistory.search([('calendar_event_id', '=', self.id), ('partner_id', '=', partner_id.id), ('attendance_state', '=', 'checked_in'), ('left_datetime', '=', False)], limit=1)
			if attendance_state == 'checked_in' and not participant_history_id:
				participant_history_id = ParticipantHistory.create({'name': partner_id.name,
																	'partner_id': partner_id.id,
																	'join_datetime': action_date,
																	'attendance_state': 'checked_in',
																	'calendar_event_id': self.id})
			elif attendance_state == 'checked_out' and participant_history_id:
				participant_history_id.write({'left_datetime': action_date,
											  'attendance_state': 'checked_out'})
		self._notify_channel_attendance()
		return participant_history_id

	def get_login_user_attendance_state(self, partner_id=False):
		ParticipantHistory = self.env['participant.history'].sudo()
		if partner_id:
			partner_id = self.env['res.partner'].sudo().browse(int(partner_id))
		else:
			partner_id = self.env.user.partner_id
		participant_history_id = ParticipantHistory.search([('calendar_event_id', '=', self.id), ('partner_id', '=', partner_id.id), ('attendance_state', '=', 'checked_in'), ('left_datetime', '=', False)], limit=1)
		if participant_history_id:
			attendance_state = 'checked_in'
		else:
			attendance_state = 'checked_out'
		return attendance_state

	def log_outgoing_message(self, message):
		return self.sudo().message_post(body=message, author_id=self.env.user.partner_id.id, subtype='mt_note', message_type='comment')

	def action_calendar_event_send(self):
		''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
		self.ensure_one()
		template_id = self.env.ref('do_video_conference.event_calender_mail_template_send_meeting', raise_if_not_found=False)
		ctx = {
			'default_model': 'calendar.event',
			'default_res_ids': self.ids,
			'default_use_template': bool(template_id),
			'default_template_id': template_id.id,
			'default_composition_mode': 'comment',
			'force_email': True,
		}
		return {
			'type': 'ir.actions.act_window',
			'view_mode': 'form',
			'res_model': 'mail.compose.message',
			'views': [(False, 'form')],
			'view_id': False,
			'target': 'new',
			'context': ctx,
		}

	def create_bigbluebutton_meeting(self):
		if not self.bbb_meeting_id:
			raise ValidationError(_("Please Set Unqiue Big Blue Buttong Session Id"))
		bigbluebutton_url = self.env['ir.config_parameter'].sudo().get_param('bigbluebutton.url', default='https://meeting.freeday15.it/bigbluebutton/')
		bigbluebutton_secret = self.env['ir.config_parameter'].sudo().get_param('bigbluebutton.secret', default='N3ltgKfWfGJr9Ui0Iz8QNpGGTUUssbzSlOJZhLuJ8')
		b = BigBlueButton(bigbluebutton_url, bigbluebutton_secret)
		bb_dicts = {}
		if self.name:
			bb_dicts.update({'name': self.name})
		if self.bbb_attendeePW:
			bb_dicts.update({'attendeePW': self.bbb_attendeePW})
		if self.bbb_moderatorPW:
			bb_dicts.update({'moderatorPW': self.bbb_moderatorPW})
		if self.bbb_allow_to_record_meeting:
			bb_dicts.update({'record': self.bbb_allow_to_record_meeting})
		if self.bbb_allow_start_stop_recording:
			bb_dicts.update({'allowStartStopRecording': self.bbb_allow_start_stop_recording})
		if self.bbb_auto_start_recording:
			bb_dicts.update({'autoStartRecording': self.bbb_auto_start_recording})
		if self.bbb_mute_on_start:
			bb_dicts.update({'muteOnStart': self.bbb_mute_on_start,
							 'allowModsToUnmuteUsers': True})
		# bb_dicts.update({'webcamsOnlyForModerator': False})
		bbb_module = None
		if self.bbb_default_presentation:
			bbb_module = BBBModule()
			bbb_module.add_slide('base64s', self.bbb_default_presentation.decode(), name=self.bbb_default_presentation_name)
		b.create_meeting(self.bbb_meeting_id, params=bb_dicts, slides=bbb_module)
		return True

	def join_bigbluebutton_meeting(self, password=False):
		if not self.bbb_meeting_id:
			raise ValidationError(_("Please Set Unqiue Big Blue Buttong Session and Create Big Blue Button Session"))
		bigbluebutton_url = self.env['ir.config_parameter'].sudo().get_param('bigbluebutton.url', default='https://meeting.freeday15.it/bigbluebutton/')
		bigbluebutton_secret = self.env['ir.config_parameter'].sudo().get_param('bigbluebutton.secret', default='N3ltgKfWfGJr9Ui0Iz8QNpGGTUUssbzSlOJZhLuJ8')
		b = BigBlueButton(bigbluebutton_url, bigbluebutton_secret)
		try:
			b.get_meeting_info(self.bbb_meeting_id)
		except Exception as e:
			_logger.exception(e)
			if not self.closed:
				self.create_bigbluebutton_meeting()
		if password and self.bbb_moderatorPW == password:
			join_url = b.get_join_meeting_url(self.env.user.name, self.bbb_meeting_id, self.bbb_moderatorPW)
		else:
			join_url = b.get_join_meeting_url(self.env.user.name, self.bbb_meeting_id, self.bbb_attendeePW)
		return join_url

	def get_bigbluebutton_meeting_recording(self):
		all_recordings = []
		if not self.bbb_meeting_id:
			raise ValidationError(_("Please Set Unqiue Big Blue Buttong Session and Create Big Blue Button Session"))
		bigbluebutton_url = self.env['ir.config_parameter'].sudo().get_param('bigbluebutton.url', default='https://meeting.freeday15.it/bigbluebutton/')
		bigbluebutton_secret = self.env['ir.config_parameter'].sudo().get_param('bigbluebutton.secret', default='N3ltgKfWfGJr9Ui0Iz8QNpGGTUUssbzSlOJZhLuJ8')
		b = BigBlueButton(bigbluebutton_url, bigbluebutton_secret)
		try:
			bb_recoring = b.get_recordings(self.bbb_meeting_id)
			for recording in bb_recoring.get('xml').get('recordings').get('recording'):
				all_recordings.append({'meetingID': recording['meetingID'],
										'participants': recording.get('participants'),
										'images': recording.get('playback').get('format').get('preview').get('images').get('image'),
										'size': recording.get('playback').get('format').get('size'),
										'type': recording.get('playback').get('format').get('type'),
										'url': recording.get('playback').get('format').get('url'),
										'published': recording.get('published'),
										'recordID': recording.get('recordID'),
									})

		except Exception as e:
			_logger.exception(e)
		return all_recordings

	def get_select_json_dumps(self, field_name, rec_name):
		tags = [dict(id=tag.id, name=tag[rec_name]) for tag in self[field_name]]
		tags = json.dumps(tags or {})
		return tags

	def create_attachment_history_line(self, partner_id, type, attachment_id, **kwargs):
		action_date = fields.Datetime.now()
		values = {'name': partner_id,
					'partner_id': partner_id,
					'type': type,
					'action_date': action_date,
					'attachment_id': attachment_id,
					'calendar_event_id': self.id
				}
		self.env['meeting.attachment.history'].sudo().create(values)
		return True

	def get_interval(self, format_type, tz=None):
		"""
		Returns a formatted interval based on the format_type and timezone.

		Args:
			format_type (str): The type of format to return. Options include 'dayname', 'day', 'month', and 'time'.
			tz (str): The timezone to use for formatting. Defaults to UTC if not provided.

		Returns:
			str: A formatted string based on the format_type and timezone.
		"""
		if tz:
			timezone = pytz.timezone(tz)
			start_date_tz = self.start.astimezone(timezone)
		else:
			start_date_tz = self.start

		if format_type == 'dayname':
			return start_date_tz.strftime('%A')  # Returns the day name (e.g., 'Monday')
		elif format_type == 'day':
			return start_date_tz.strftime('%d')  # Returns the day of the month (e.g., '01')
		elif format_type == 'month':
			return start_date_tz.strftime('%B')  # Returns the full month name (e.g., 'January')
		elif format_type == 'time':
			return start_date_tz.strftime('%H:%M')  # Returns the time in HH:MM format
		else:
			raise ValueError(f"Unsupported format_type: {format_type}")