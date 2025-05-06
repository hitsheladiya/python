from odoo import models, fields, api, _

class SalesMarge(models.Model):
	_inherit = "sale.order"

	def sales_marge_buttom(self):
		action = self.env.ref("merge_so_lines_app.action_marge_sales_wizard").read()[0]
		return action
		