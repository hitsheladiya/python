from odoo import models, fields, api
from odoo.exceptions import AccessError

class SaleOrder(models.Model):
	_inherit = "sale.order"

	amount = fields.Float(string="Amount")

	def action_confirm(self):
		
		if not self.env.user.has_group('skylark_credit_limit_approval.group_credit_limit_approval'):
			raise AccessError("You do not have permission to request a credit limit increase.")
		
		for order in self:
			customer = order.partner_id
			credit_limit = customer.credit_limit or 0
			if order.amount_total > credit_limit:
				return {
					'type': 'ir.actions.act_window',
					'name': 'Credit Limit Request',
					'res_model': 'credit.limit.wizard',
					'view_mode': 'form',
					'target': 'new',
					'context': {
						'default_customer_id': customer.id,
						'default_credit_limit': credit_limit,
						'default_increase_credit': order.amount_total - credit_limit,
						'default_message': '',
					}
				}

		return super(SaleOrder, self).action_confirm()


	def action_view_delivery(self):

		for picking in self.picking_ids:
			picking.amount = self.amount

		return super(SaleOrder, self).action_view_delivery()

