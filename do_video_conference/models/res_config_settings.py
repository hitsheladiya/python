# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	jitsi_meet_url = fields.Char(string='JITSI Meet URL', help='JITSI Meet URL like: https://meet.jit.si/', readonly=False)
	jitsi_meet_domain = fields.Char(string='JITSI Meet Domain', help='JITSI Meet Domain Like : meet.jit.si', readonly=False)
	bigbluebutton_url = fields.Char(string='BigBlueButton URL', help='BigBlueButton URL like : https://yourdomain.com/bigbluebutton/', readonly=False)
	bigbluebutton_secret = fields.Char(string='BigBlueButton Secret Key', help='BigBlueButton Secret key you can get it from https://docs.bigbluebutton.org/admin/bbb-conf.html', readonly=False)

	@api.model
	def get_values(self):
		res = super(ResConfigSettings, self).get_values()
		res['jitsi_meet_url'] = self.env['ir.config_parameter'].sudo().get_param('jitsi.server')
		res['jitsi_meet_domain'] = self.env['ir.config_parameter'].sudo().get_param('jitsi.server.domain')
		res['bigbluebutton_url'] = self.env['ir.config_parameter'].sudo().get_param('bigbluebutton.url')
		res['bigbluebutton_secret'] = self.env['ir.config_parameter'].sudo().get_param('bigbluebutton.secret')
		return res

	@api.model
	def set_values(self):
		self.env['ir.config_parameter'].sudo().set_param('jitsi.server', self.jitsi_meet_url)
		self.env['ir.config_parameter'].sudo().set_param('jitsi.server.domain', self.jitsi_meet_domain)
		self.env['ir.config_parameter'].sudo().set_param('bigbluebutton.url', self.bigbluebutton_url)
		self.env['ir.config_parameter'].sudo().set_param('bigbluebutton.secret', self.bigbluebutton_secret)
		super(ResConfigSettings, self).set_values()