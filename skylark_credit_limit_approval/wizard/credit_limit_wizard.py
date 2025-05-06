from odoo import models, fields, api

class CreditLimitWizard(models.TransientModel):
	_name = 'credit.limit.wizard'
	_description = 'Credit Limit Request Wizard'

	customer_id = fields.Many2one('res.partner', string="Customer", required=True)
	credit_limit = fields.Float(string="Your Current Credit Limit", readonly=True)
	increase_credit = fields.Float(string="Increase Credit Amount")
	message = fields.Text(string="Message")
	warning_message = fields.Text(string="Warning Message", compute="_compute_warning_message")

	@api.depends('customer_id')
	def _compute_warning_message(self):
		for wizard in self:
			if wizard.customer_id:
				pending_requests = self.env['credit.limit.request'].search_count([
					('customer_id', '=', wizard.customer_id.id),
					('state', '=', 'pending')
				])
				if pending_requests:
					wizard.warning_message = "You already have a pending request in pending state. Please wait for approval before submitting a new request."
				else:
					wizard.warning_message = f"Sorry, Your Current Limit Is {wizard.credit_limit}. You Need To Send a Request To Increase Your Limit."

	def action_submit_request(self):
		existing_pending = self.env['credit.limit.request'].search([
			('customer_id', '=', self.customer_id.id),
			('state', '=', 'pending')
		])
		if existing_pending:
			raise models.ValidationError("You cannot submit another request while a pending request is pending.")
		vals = {
			'customer_id': self.customer_id.id,
			'requested_credit_limit': self.increase_credit,
			'message': self.message,
			'state': 'pending'
		}
		self.env['credit.limit.request'].create(vals)
