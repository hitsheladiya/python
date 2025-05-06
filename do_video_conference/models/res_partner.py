# -*- coding: utf-8 -*-

from odoo import fields, models

class ResPartner(models.Model):
	_inherit = 'res.partner'

	meeting_otp = fields.Char(string='Session OTP')