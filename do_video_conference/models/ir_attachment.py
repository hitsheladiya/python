# -*- coding: utf-8 -*-

import mimetypes
from odoo import models

class IrAttachment(models.Model):
	_inherit = 'ir.attachment'

	def get_extension(self):
		extension = mimetypes.guess_extension(self.mimetype)
		extension = extension.replace('.', '')
		return extension