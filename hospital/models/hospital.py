from odoo import api, fields, models, _

class HospitalName(models.Model):
	_name = "hospital.hospital"
	_description = "hospital" 
	_inherit = ['mail.thread', 'mail.activity.mixin']


	name = fields.Char(string="Hospital Name", tracking=True)
	add= fields.Char(string="Address", tracking=True)
	image = fields.Binary(string="Image")
	hospital_id = fields.One2many("hospital.patient", "patient_ids", string="Patient name")
	hospitals_id = fields.One2many("hospital.doctor", "doctor_ids", string="Doctor Name")
	total_patient = fields.Integer(string="Total Patient", compute='_compute_total_patient')
	# display_name = fields.Char(string="Display Name", compute='action_compute_display_name')


	def create(self,vals):
		print("......self", self)
		print("......vals", vals)
		cr = super(HospitalName, self).create(vals)
		print(".....cr", cr)

		hospital_serch = self.env['hospital.hospital'].search([])
		print("\nhospital id.....", hospital_serch)	
		rd = hospital_serch.read(fields=["name", "add"])
		print(".....rd",rd)

		hospital = self.env['hospital.hospital']
		print('\n.......self', self)
		srd = hospital.search_read(fields=['name'])
		print('......search Read',srd)
		return cr


	def write(self,vals):
		print("......self", self)
		print("......vals", vals)
		wr = super(HospitalName, self).write(vals)
		print(".....wr", wr)
		hospital_browse = self.env['hospital.hospital'].browse(3)
		print(f"hospital name..... {hospital_browse.name},\nhospital Address is...... {hospital_browse.add}")

	# 	fields_info = self.env['hospital.hospital'].fields_get()
	# 	for fields_name, fields_info in fields_info.items():
	# 		print(f"field Name : {fields_name}")
	# 		print(f"Field Info : {fields_info}")
	# 	return wr



	# @api.depends('add','name')
	# def action_compute_display_name(self):
	# 	for record in self:
	# 		record.display_name = f"Hospital Name is {record.name} and Address is {record.add}"
	# 	print(".....record", record.display_name)

	def action_compute_display_name(self):
		for record in self:
			domain = [('patient_ids', '=', record.id)]
			return {
            	'type': 'ir.actions.act_window',
				'name': 'pstient Details', 
				'res_model': 'hospital.patient',  
				'view_mode': 'list,form',  # Open in form view
				'target': 'current',  # Open in the current window
				'domain':domain
				}

	@api.depends('hospital_id')
	def _compute_total_patient(self):
		for record in self:
			record.total_patient = len(record.hospital_id)



	
	# @api.model
	# def _name_search(self, name, domain=None, operator='ilike', limit=10, order=None):
	# 	domain = domain or []
	# 	print('.......name', name)
	# 	print('.....domain', domain)
	# 	print('......operator', operator)
	# 	print('.....limit', limit)
	# 	if name:
	# 		domain+=['|',('name', 'ilike', name), ('add', 'ilike', name)]
	# 	print("domain.......",domain)
	# 	return self._search(domain, limit=limit, order=order)			