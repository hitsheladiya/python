# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval, time
from odoo.osv import expression
from odoo.exceptions import AccessError, ValidationError

class GlobalSearchWizard(models.TransientModel):
	_name = "global.search.wizard"
	_description = "Global Search Wizard"

	model_id = fields.Many2one("ir.model","Model")
	model_name = fields.Char(related="model_id.model",string="Model Name")
	domain = fields.Text("Domain")

	@api.onchange("model_id")
	def onchange_on_domain(self):
		for rec in self:
			if self._context.get("change_from_field"):
				rec.domain = ""

	def default_get(self,fields):
		res = super().default_get(fields)
		if self._context.get("default_model_name"):
			model_id = self.env['ir.model'].search([('model','=',self._context.get("default_model_name"))])
			if model_id:
				res['model_id'] = model_id.id 
		return res

	def set_domain(self):
		pass

	def action_open(self):
		self.ensure_one()	
		model_name = self.model_id.model
		if not model_name:
			return

		domain = eval(self.domain) if self.domain else []
		action = self.env["ir.actions.act_window"].search([('res_model', '=', model_name),('view_mode', 'like', 'list')], limit=1)

		if not action:
			return

		return {
			"type": "ir.actions.act_window",
			"name": action.name or "View Records",
			"res_model": model_name,
			"view_mode": "list,form",
			"domain": domain,
			"context": {"search_default_group_by": 1},
			"target": "current",
		}

	@api.model
	def _eval_context(self):
		return {
			'user': self.env.user.with_context({}),
			'time': time,
			'company_ids': self.env.companies.ids,
			'company_id': self.env.company.id,
		}

	@api.constrains('domain', 'model_id')
	def _check_domain(self):
		eval_context = self._eval_context()
		for rec in self:
			if rec.domain:
				try:
					domain = safe_eval(rec.domain, eval_context)
					expression.expression(domain, self.env[rec.model_id.model].sudo())
				except Exception as e:
					raise ValidationError(_('Invalid domain: %s', e))