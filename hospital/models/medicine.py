from odoo import api, fields, models, _

class HospitalMedicin(models.Model):
	_name = "hospital.medicine"
	_description = "medicine"
	_rec_name = "name"
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Char(string="Medicine", tracking=True)
	medicine_index = fields.Integer(string="Medicne Id", tracking=True)
	medicin_ids = fields.Many2one("hospital.patient", string= "Patient Name")

	@api.model
	def name_search(self, name, args=None, operator='ilike', limit=10):
		args = args or []
		print('.......name', name)
		print('.....args', args)
		print('......operator', operator)
		print('.....limit', limit)

		if name:
			rec = self.search(['|', ('name', operator, name), ('medicine_index', operator, name)], limit=limit)
			return [(record.id, record.name) for record in rec]
		return super().name_search(name, args, operator, limit)