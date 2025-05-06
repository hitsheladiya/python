from odoo import models, fields, api

class CreditLimitRequest(models.Model):
	_name = 'credit.limit.request'
	_description = 'Credit Limit Request'
	_rec_name = "customer_id"

	customer_id = fields.Many2one('res.partner', string="Customer", required=True)
	current_credit_limit = fields.Float(string="Current Credit Limit", compute='_compute_current_credit_limit', store=True)
	requested_credit_limit = fields.Float(string="Increase Amount", required=True)
	message = fields.Text(string="Message")
	state = fields.Selection([
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Status", default="pending")

	@api.depends('customer_id.credit_limit')
	def _compute_current_credit_limit(self):
		for record in self:
			record.current_credit_limit = record.customer_id.credit_limit

	def action_approve(self):
		for record in self:
			if record.customer_id:
				new_limit = record.customer_id.credit_limit + record.requested_credit_limit
				record.customer_id.write({'credit_limit': new_limit})
				record.current_credit_limit = new_limit 
			record.state = 'approved'

	def action_cancel(self):
		for record in self:
			record.state = 'rejected'
