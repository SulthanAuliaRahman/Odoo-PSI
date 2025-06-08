from odoo.exceptions import UserError
from odoo import api, fields, models, _
from odoo.addons.pos_discount.models.pos_config import PosConfig as DiscountConfig
# Remove pos_discount open_ui function to recode it in our custom module
del DiscountConfig.open_ui


class PosConfig(models.Model):
    _inherit = 'pos.config'

    discount_limit = fields.Boolean(string="Discount Limit")
    discount_limit_pc = fields.Float(string="Discount Limit (%)")
    is_discount_fixed = fields.Boolean(string="Is Discount Fixed")
    discount_line_limit = fields.Boolean("Discount Line limit")
    discount_line_limit_pc = fields.Float("Discount Line Limit (%)")
    apply_on = fields.Selection(string="Apply On", selection=[
        ('lines', 'lines'), ('order', 'Order')], required=True, default="lines")
    allow_global_discount_apply_on = fields.Boolean(
        related="company_id.allow_global_discount_apply_on", readonly=False)

    def open_ui(self):
        for config in self:
            if (not config.current_session_id and config.module_pos_discount
                    and not config.discount_product_id and config.apply_on == 'order'):
                raise UserError(
                    _('A discount product is needed to use the Global Discount feature. Go to Point of Sale > Configuration > Settings to set it.'))
        return super().open_ui()
