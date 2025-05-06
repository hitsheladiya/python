# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID
from odoo.http import request
from odoo.addons.bus.controllers.main import BusController

class MeetingChatController(BusController):

	def _default_request_uid(self):
		""" For Anonymous people, they receive the access right of SUPERUSER_ID since they have NO access (auth=none)
			!!! Each time a method from this controller is call, there is a check if the user (who can be anonymous and Sudo access)
			can access to the resource.
		"""
		return request.session.uid and request.session.uid or SUPERUSER_ID

	# --------------------------
	# Extends BUS Controller Poll
	# --------------------------
	def _poll(self, dbname, channels, last, options):
		if request.session.uid:
			channels = list(channels)
			channels.append((request.db, 'calendar.event', request.env.user.partner_id.id))
		return super(MeetingChatController, self)._poll(dbname, channels, last, options)