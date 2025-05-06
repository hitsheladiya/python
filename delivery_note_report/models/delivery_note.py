from odoo import models, fields, api

class DeliveryNote(models.Model):
    _name = 'natuber.delivery.note'
    _description = 'Natuber Delivery Note'

    name = fields.Char(string='Delivery Note Number', required=True)
    order_id = fields.Many2one('sale.order', string='Order')
    partner_id = fields.Many2one('res.partner', string='Customer')
    date_order = fields.Datetime(related='order_id.date_order', string='Order Date')
    order_line = fields.One2many(related='order_id.order_line', string='Products')
    client_order_ref = fields.Char(related='order_id.client_order_ref', string='Customer Reference')
    base_2 = fields.Monetary(string="Base 2%", currency_field="currency_id")
    iva_2 = fields.Monetary(string="IVA 2%", currency_field="currency_id")
    base_10 = fields.Monetary(string="Base 10%", currency_field="currency_id")
    iva_10 = fields.Monetary(string="IVA 10%", currency_field="currency_id")
    total = fields.Monetary(string="Total", compute="_compute_total", currency_field="currency_id")

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id.id
    )
    invoice_line_ids = fields.One2many(
        comodel_name="account.move.line",
        compute="_compute_invoice_lines",
        string="Invoice Lines"
    )
    amount_untaxed = fields.Monetary(
        string="Untaxed Amount",
        compute="_compute_amounts",
        currency_field="currency_id",
        store=True
    )

    amount_tax = fields.Monetary(
        string="Taxes",
        compute="_compute_amounts",
        currency_field="currency_id",
        store=True
    )

    amount_total = fields.Monetary(
        string="Total",
        compute="_compute_amounts",
        currency_field="currency_id",
        store=True
    )

    @api.depends('order_id.amount_untaxed', 'order_id.amount_tax', 'order_id.amount_total')
    def _compute_amounts(self):
        for record in self:
            record.amount_untaxed = record.order_id.amount_untaxed if record.order_id else 0.0
            record.amount_tax = record.order_id.amount_tax if record.order_id else 0.0
            record.amount_total = record.order_id.amount_total if record.order_id else 0.0
    @api.depends('order_id.invoice_ids.invoice_line_ids')
    def _compute_invoice_lines(self):
        for record in self:
            invoices = record.order_id.invoice_ids.filtered(lambda inv: inv.state == 'posted')
            record.invoice_line_ids = invoices.mapped('invoice_line_ids')
    @api.depends('base_2', 'iva_2', 'base_10', 'iva_10')
    def _compute_total(self):
        for record in self:
            record.total = (record.base_2 or 0.0) + (record.iva_2 or 0.0) + (record.base_10 or 0.0) + (record.iva_10 or 0.0)