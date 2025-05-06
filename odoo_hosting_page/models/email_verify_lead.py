from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    otp = fields.Char(string="OTP")
    selected_plan = fields.Selection([
        ('free', 'Free Plan'),
        ('paid', 'Paid Plan'),
    ], string='Selected Plan')

    def mark_lead_verified(self):
        verified_tag = self.env['crm.tag'].sudo().search([('name', '=', 'Verified')], limit=1)
        if not verified_tag:
            verified_tag = self.env['crm.tag'].sudo().create({'name': 'Verified'})
        self.write({'tag_ids': [(4, verified_tag.id)]})

    def mark_lead_not_verified(self):
        not_verified_tag = self.env['crm.tag'].sudo().search([('name', '=', 'Not Verified')], limit=1)
        if not not_verified_tag:
            not_verified_tag = self.env['crm.tag'].sudo().create({'name': 'Not Verified'})
        self.write({'tag_ids': [(4, not_verified_tag.id)]})
