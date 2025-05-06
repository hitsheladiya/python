from odoo import api, fields, models, _

class HospitalDoctor(models.Model):
	_name = "hospital.doctor"
	_description = "doctor"
	_rec_name ="name"
	_inherit = ['mail.thread', 'mail.activity.mixin']



	name = fields.Char(string="Name", default="zalak patel", tracking=True)
	type = fields.Char(string="Doctor Type", default="general", tracking=True)
	doctor_ids = fields.Many2one("hospital.hospital", string="Hospital Details")
	image = fields.Binary(string="Image")


	# def create(self,vals):
	# 	print('.....self', self)
	# 	print("....vals",vals )	
	# 	cr = super(HospitalDoctor, self).create(vals)
	# 	print('......cr', cr)
	# 	return cr


	# def write(self,vals):
		# 	print('.....self', self)
	# 	print('.....vals', vals)
	# 	rtn = super(HospitalDoctor, self).write(vals)
	# 	print('......rtn', rtn)
	# 	return rtn


	# def unlink(self):
	# 	print('.....self', self)
	# 	un = super(HospitalDoctor, self).unlink()
	# 	print('.....un', un)
	# 	return un


	# def copy(self, default = {}):
	# 	print('....self', self)
	# 	print('.....default', default)
	# 	co = super(HospitalDoctor, self).copy(default=default)
	# 	print('.....co',co)
	# 	return co

	# def default_get(self, field_list=[]):
	# 	print('.....field_list', field_list)
	# 	df = super(HospitalDoctor, self).default_get(field_list)
	# 	print('.....df', df)
	# 	df['type'] = 'MD'
	# 	ct = self.env['hospital.doctor'].search_count([('name', '=', 'zalak patel')])
	# 	print('.....count', ct)

	# cts = self.env['hospital.doctor'].search([])
	# 	print('.....search', cts)

	# hospital_browse = self.env['hospital.hospital'].search([('name', '=', 'Shelby')])
	# 	print("hospital id.....", hospital_browse)	
	# 	return df	

