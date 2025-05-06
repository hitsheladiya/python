# -- coding: utf-8 --

from odoo import models, fields, api,_

class HospitalWizard(models.TransientModel):
	_name = "hospital.patient.wizard"
	_description = "Patient Wizard Details"

	name = fields.Char(string="Patient Name")
	mobile_number = fields.Char(string="Mobile Number")
	dob = fields.Date(string="Date Of Birth")