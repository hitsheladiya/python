from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    credit_limit = fields.Float(string="Credit Limit")
