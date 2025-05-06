# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class HospitalName(models.Model):
	_name = "hospital.hospital"
	_description = "This Is Hospital Details"
	_inherit = ['mail.thread','mail.activity.mixin']

	name = fields.Char(string="Hospital Name",tracking=True)
	add = fields.Text(string="Address", tracking=True)
	hospital_code = fields.Integer(string="Hospital Id",tracking=True)
	hospital_doctor_ids = fields.One2many("hospital.doctor","doctor_id",string="Doctor Name")
	hospital_patient_ids = fields.One2many("hospital.patient","patient_id",string="Patient Name")
	hospital_appointment_ids= fields.One2many("hospital.appointment","appointment_id",string="Appointment Patient Name")
	image_hospital = fields.Binary(string="Hospital")
	email = fields.Char(string="Email")
	phone = fields.Char(string="Contact")
	patient_details = fields.Char(string="Display name", compute="action_compute_display_name",store=True)
	total_patient = fields.Integer(string="Total Patient", compute='_compute_total_patient')


	def create(self,vals):
		lr=super(HospitalName,self).create(vals)
		return lr


	def write(self,vals):
		lr=super(HospitalName,self).write(vals)
		return lr

	def unlink(self):
		lr = super(HospitalName, self).unlink() 
		return lr

	@api.model
	def name_search(self, name, args=None, operator='ilike', limit=10):
		args = args or []
		if name:
			rec = self.search(['|', ('name', operator, name), ('hospital_code', operator, name)], limit=limit)
			return [(record.id, record.name) for record in rec]
		return super().name_search(name, args, operator, limit)


	def action_compute_display_name(self):
		for record in self:
			domain = [('patient_id', '=', record.id)]
			return {
					'type' : 'ir.actions.act_window',
					'name' : 'Patient Details',
					'res_model' : 'hospital.patient',
					'view_mode' : 'list,form',
					'target' : 'current',
					'domain' : domain
				}

	@api.depends('hospital_patient_ids')
	def _compute_total_patient(self):
		for record in self:
			record.total_patient = len(record.hospital_patient_ids)
