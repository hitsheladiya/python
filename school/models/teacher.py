# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SchoolTeacher(models.Model):
	_name = 'school.teacher'

	name = fields.Char(string="Teacher Name")
	course_ids = fields.Many2many("school.course",string="Course Name")