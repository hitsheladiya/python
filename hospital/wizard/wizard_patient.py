from odoo import api, fields, models, _

class HospitalWizard(models.TransientModel):
	_name = "hospital.wizard"
	_description = "wizard"




	name = fields.Char(string=" Patient Name")
	age = fields.Integer(string="Age")

	# def create_patient(self):
	# 	self.env['hospital.patient'].create({
	# 		'name': self.name,
	# 		'age': self.age
	# 	})
	# 	return {'type': 'ir.actions.act_window_close'}


	def update_patient(self):
		patient = self.env['hospital.patient'].search([
			('name', '=', self.name)
			# ... any other fields ...
		], limit=1)

		if patient:
			patient.write({
				"name" : self.name,
				"age" : self.age
			})
		return {'type': 'ir.actions.act_window_close'}

	