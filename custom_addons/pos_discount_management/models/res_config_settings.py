from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    allow_global_discount_apply_on = fields.Boolean(related="company_id.allow_global_discount_apply_on", readonly=False)
