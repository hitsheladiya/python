# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class DoctorDetails(models.Model):
	_name = "hospital.doctor"
	_description = "This Is Doctor Details"
	_rec_name = "name"
	_inherit = ["mail.thread","mail.activity.mixin"]

	name = fields.Char(string="Doctor Name",tracking=True)
	doctor_type = fields.Char(string="Doctor Type",tracking=True)
	doctor_id = fields.Many2one("hospital.hospital",string="Hospital Name")
	image_doctor = fields.Binary(string="Doctor")
	doctor_gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
	mobile_number = fields.Char(string="Mobile Number",tracking=True)
	doctor_age = fields.Integer(string="Age",tracking=True)
	doctor_appo_patient_id = fields.Many2one("hospital.appointment",string="Appointment Details")




	def create(self,vals):
		qr=super(DoctorDetails,self).create(vals)
		return qr


	def write(self,vals):
		qr=super(DoctorDetails,self).write(vals)
		return qr

	def unlink(self):
		qr = super(DoctorDetails, self).unlink()   
		return qr

