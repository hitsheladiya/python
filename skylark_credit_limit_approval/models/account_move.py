from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
	_inherit = 'account.move'

	def action_post(self):
		for move in self:
			if move.move_type == 'out_invoice': 
				customer = move.partner_id
				credit_limit = customer.credit_limit or 0 
				total_due = move.amount_total + customer.credit 
				
				if total_due > credit_limit:
					return {
						'type': 'ir.actions.act_window',
						'name': 'Credit Limit Request',
						'res_model': 'credit.limit.wizard',
						'view_mode': 'form',
						'target': 'new',
						'context': {
							'default_customer_id': customer.id,
							'default_credit_limit': credit_limit,
							'default_increase_credit': total_due - credit_limit,
							'default_message': '',
						}
					}
		
		return super(AccountMove, self).action_post()
