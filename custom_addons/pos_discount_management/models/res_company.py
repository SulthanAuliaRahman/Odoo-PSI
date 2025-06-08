from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    allow_global_discount_apply_on = fields.Boolean( string="Allow change global discount apply on", default=False)
