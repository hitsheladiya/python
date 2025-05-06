from odoo import api, fields, models, _
# from random import randint	


class HospitalPatient(models.Model):
	_name = "hospital.patient"
	_description = "patient"
	_rec_name = "name"
	_inherit = ['mail.thread']

	
	name = fields.Char(string=" Patient Name", tracking=True)
	age = fields.Integer(string="Age", tracking=True)
	mobile_no = fields.Char(string="Mobile No", tracking=True)
	gender = fields.Selection([('male', 'Male'),('female', "Female")], string = "gender", tracking=True)
	patient_ids = fields.Many2one("hospital.hospital", string="Hospital Details")
	patients_ids = fields.Many2many("hospital.medicine", "medicin_ids", string="Medicine Name")
	image = fields.Binary(string="Image")
	date = fields.Datetime(string="Birth Date", tracking=True)
	

	def action_appointment_print(self):
		return self.env.ref('hospital.action_hospital_report').report_action(self)
	
						

	def action_compute_display_name(self):
		for student in self:
			domain = [('hospital_id', '=', record.id)]  # Filter students related to this school
			return {
				'type': 'ir.actions.act_window',
				'name': 'School Details', 
				'res_model': 'hospital.hospital',  
				'view_mode': 'list,form',  # Open in form view
				'target': 'current',  # Open in the current window
				}




