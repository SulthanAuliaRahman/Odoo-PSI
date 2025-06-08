from odoo import fields, models


class ProductsRestrict(models.Model):
    """Inherited product.template"""
    _inherit = 'product.template'

    is_age_restrict = fields.Boolean(
        string="Is Age Restricted",
        help="By enabling this, product will require minimum age to be purchased."
    )
    min_age_required = fields.Text(
        string="Minimum Age Required",
        default=18,
        help="Minimum age required to purchase this product."
    )
