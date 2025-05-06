# -- coding: utf-8 --

from odoo import models, fields, api,_

class SalesWizard(models.TransientModel):
	_name = "marge.sales.wizard"
	_description = "My Wizard"

	
	def action_merge_lines(self):
		sale_order_ids = self.env['sale.order'].browse(self.env.context['active_ids'])
		print("---self.context---",self.env.context)
		print("sale_order_ids-----",sale_order_ids)
		for order in sale_order_ids:
			grouped_lines = {}
			for line in order.order_line:
				key = (line.product_id.id)
				print("key-----",key)
				if key not in grouped_lines:
					grouped_lines[key] = line
					print("---group---",grouped_lines)
				else:
					grouped_lines[key].product_uom_qty += line.product_uom_qty
					grouped_lines[key].price_unit = (grouped_lines[key].price_unit + line.price_unit) / 2
					print("----lines-key-----",grouped_lines[key].price_unit)
					line.unlink()