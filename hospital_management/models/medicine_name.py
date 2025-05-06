# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from random import randint
	
class MedicineName(models.Model):
	_name = "hospital.medicinename"
	_rec_name = "name"
	_description = "This Is Medicine Name"
	_inherit = ['mail.thread','mail.activity.mixin']

	def _get_default_color(self):
		return randint(1, 11)

	name = fields.Char(string="Medicine Name", tracking=True)
	medicine_index = fields.Integer(string="Medicine Id", tracking=True)
	patient_medicine_id = fields.Many2one("hospital.patient", string="Patient")  # Adjusted field name
	color = fields.Integer(string='Color', default=_get_default_color, aggregator=False)


	def create(self,vals):
		er=super(MedicineName,self).create(vals)
		return er


	def write(self,vals):
		er=super(MedicineName,self).write(vals)
		return er

	def unlink(self):
		er = super(MedicineName, self).unlink() 
		return er










class MedicineName(models.Model):
	_name = "hospital.medicinename"
	_rec_name = "name"
	_description = "This Is Medicine Name"
	_inherit = ['mail.thread','mail.activity.mixin']

	def _get_default_color(self):
		return randint(1, 11)

	name = fields.Char(string="Medicine Name", tracking=True)
	medicine_index = fields.Integer(string="Medicine Id", tracking=True)
	patient_medicine_id = fields.Many2one("hospital.patient", string="Patient")  # Adjusted field name
	color = fields.Integer(string='Color', default=_get_default_color, aggregator=False)
