# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SchoolClass(models.Model):
	_name = "school.class"
	_rec_name = "name"
	
	name = fields.Char(string="Class Name")
	course_id = fields.Many2one('school.course',string='Course Name')
	student_ids = fields.Many2many('school.student','class_id', string="Student Name")
	student_id = fields.One2many("school.student","nick_ids",string="Nick Name")