from odoo import models, fields, api

class SaleOrder(models.Model):
	_inherit = "stock.picking"

	amount = fields.Float(string="Amount")
