# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class PatientDetail(models.Model):
	_name = "hospital.patient"
	_rec_name = "name"
	_description = "This Is Patient Details"
	_inherit = ['mail.thread','mail.activity.mixin']

	name = fields.Char(string="Patient Name")
	mobile_numbers = fields.Char(string="Mobile Number",tracking=True)
	age = fields.Integer(string="Age", tracking=True)
	gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
	patient_id = fields.Many2one("hospital.hospital",string="Hospital Name")
	image = fields.Binary(string="Image")
	appointment_ids = fields.One2many("hospital.appointment", "patients_id", string="Appointments")
	medicine_name_ids = fields.Many2many("hospital.medicinename","patient_medicine_id",string="Medicine name")


	def create(self,vals):
		ar=super(PatientDetail,self).create(vals)
		patients = self.env['hospital.patient'].search([])
		patient = patients.read(fields=['name','gender','mobile_numbers'])
		return ar


	def write(self,vals):
		ar=super(PatientDetail,self).write(vals)
		return ar

	def unlink(self):
		ar = super(PatientDetail, self).unlink() 
		return ar


	@api.model
	def name_search(self, name, args=None, operator='ilike', limit=10):
		args = args or []
		if name:
			rec = self.search(['|', ('name', operator, name), ('mobile_numbers', operator, name)], limit=limit)
			return [(record.id, record.name) for record in rec]
		return super().name_search(name, args, operator, limit)
