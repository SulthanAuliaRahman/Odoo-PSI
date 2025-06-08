from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    auto_print_receipt = fields.Boolean("Cetak struk otomatis")
