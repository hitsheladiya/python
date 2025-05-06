from odoo import models, api, exceptions

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.constrains('groups_id')
    def _check_unique_access(self):
        access_groups = [
            'retail_access_rights.group_cashier',
            'retail_access_rights.group_inventory_staff',
            'retail_access_rights.group_store_manager',
            'retail_access_rights.group_admin'
        ]
        for user in self:
            count = sum(1 for group in access_groups if user.has_group(group))
            if count > 1:
                raise exceptions.ValidationError("A user can only have one access right at a time.")
