# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SchoolCourse(models.Model):
	_name = 'school.course'

	name = fields.Char(string="Course Name")
	school_id = fields.Many2one('school.school',sting="School Name")
	class_ids = fields.Many2many('school.class','course_id',string="Class Name")
	teacher_ids = fields.Many2many('school.teacher',sting="Teacher Name")