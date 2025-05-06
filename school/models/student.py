# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SchoolStudent(models.Model):
	_name = 'school.student'

	name = fields.Char(string="Student Name")
	roll_number = fields.Integer(string="Student Roll.")
	class_id = fields.Many2one('school.class',string="Class Name")
	nick_ids = fields.Many2one('school.class', string='Nick Name')