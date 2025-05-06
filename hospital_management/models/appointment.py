# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class HospitalAppointment(models.Model):
	_name = "hospital.appointment"
	_description = "This Is Use For Appointment"
	_inherit = ["mail.thread","mail.activity.mixin"]

	status = fields.Char(string="Status")
	date_time = fields.Datetime(string="Date-Time")
	appointment_id = fields.Many2one("hospital.hospital",string="Hospital Name")
	patients_id = fields.Many2one("hospital.patient", string="Patient Name", tracking=True)
	display_name = fields.Char(string="Display Name", compute='_compute_display_name', store=True)

	def create(self,vals):
		cr=super(HospitalAppointment,self).create(vals)
		ct = self.env['hospital.appointment'].search_count([('patients_id', '=', 'Hit Sheladiya')])
		sr = self.env['hospital.appointment'].search([('patients_id','=','Hit Sheladiya')])
		return cr


	def write(self,vals):
		
		cr=super(HospitalAppointment,self).write(vals)
		return cr

	def unlink(self):
		cr = super(HospitalAppointment, self).unlink() 
		return cr

	def copy(self, default = {}):
		default['patients_id']="Zalak Sidapara"
		cr = super(HospitalAppointment, self).copy(default=default)
		return cr

	def copy(self, default = None):
		cr = super(HospitalAppointment, self).copy(default=default)
		return cr

	@api.depends('date_time','patients_id')
	def _compute_display_name(self):
		for record in self:
			record.display_name = f"Appointment with {record.patients_id.name} on {record.date_time}"
