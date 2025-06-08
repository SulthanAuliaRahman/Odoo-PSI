from odoo import models


class PosSession(models.Model):
    """Inherited Pos Session"""
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        """Loaded the field to POS frontend"""
        result = super()._loader_params_product_product()
        result['search_params']['fields'].extend(['is_age_restrict', 'min_age_required'])
        return result