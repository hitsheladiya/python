# -*- coding: utf-8 -*-

from odoo import models, fields, api , _

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    report_password = fields.Char("Password")