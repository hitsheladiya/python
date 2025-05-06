# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PosConfig(models.Model):
	_inherit = 'pos.config'

	iface_vkeyboard = fields.Boolean(string='Virtual KeyBoard', help=u"Don’t turn this option on if you take orders on smartphones or tablets. \n Such devices already benefit from a native keyboard.")