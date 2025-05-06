# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class School(models.Model):
	_name = "school.school"

	name = fields.Char(string="School Name",default="Patel pvt schooll")
	address = fields.Char(string="Adderess")
	course_ids = fields.Many2many("school.course","school_id", string="Course Name")