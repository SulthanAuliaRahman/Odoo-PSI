import json
from odoo import api, fields, models


class PosGlobalDiscount(models.Model):
    _name = 'pos.global.discount'
    _rec_name = 'name'
    _description = 'Pos Global Discount'

    name = fields.Char(string="Name", required=True)
    discount_product_id = fields.Many2one(comodel_name="product.product", string="Discount Product")
    discount_pc = fields.Float(string="Init Discount(%)")
    is_discount_fixed = fields.Boolean(string="Is Discount Fixed")
    discount_limit = fields.Boolean(string="Discount Limit")
    discount_limit_pc = fields.Float(string="Discount Limit (%)")
    apply_on = fields.Selection(string="Apply On", selection=[
        ('lines', 'lines'), ('order', 'Order')], required=True, default="lines")
    pos_config_ids = fields.Many2many(comodel_name="pos.config", string="Point of Sale")
    pos_config_domain = fields.Char(compute="_compute_pos_config_domain")

    @api.depends('pos_config_ids')
    def _compute_pos_config_domain(self):
        for rec in self:
            ids = []
            for prev in self.search([('id', 'not in', rec.ids)]):
                ids.extend(prev.pos_config_ids.ids)
            rec.pos_config_domain = [('id', 'not in', ids)]

    @api.model
    def create(self, values):
        res = super().create(values)
        for record in res:
            # Add Discount
            for config in record.pos_config_ids:
                config.module_pos_discount = True
                config.discount_product_id = record.discount_product_id
                config.discount_pc = record.discount_pc
                config.discount_limit = record.discount_limit
                config.discount_limit_pc = record.discount_limit_pc
                config.is_discount_fixed = record.is_discount_fixed
                config.apply_on = record.apply_on
        return res

    def write(self, values):
        old_configs = self.pos_config_ids
        res = super().write(values)
        # Remove discount
        for config in (old_configs - self.pos_config_ids):
            config.module_pos_discount = False
            config.discount_product_id = False
            config.discount_pc = 0.0
            config.discount_limit = False
            config.discount_limit_pc = 0.0
            config.is_discount_fixed = False
            config.apply_on = 'lines'
        # Add Discount
        for config in self.pos_config_ids:
            config.module_pos_discount = True
            config.discount_product_id = self.discount_product_id
            config.discount_pc = self.discount_pc
            config.discount_limit = self.discount_limit
            config.discount_limit_pc = self.discount_limit_pc
            config.is_discount_fixed = self.is_discount_fixed
            config.apply_on = self.apply_on
        return res


    def unlink(self):
        for config in self.pos_config_ids:
            config.module_pos_discount = False
            config.discount_product_id = False
            config.discount_pc = 0.0
            config.discount_limit = False
            config.discount_limit_pc = 0.0
            config.is_discount_fixed = False
            config.is_discount_fixed = 'lines'
        return super().unlink()

    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        self.clear_caches()
        if view_type == 'form':
            for node in arch.xpath("//field[@name='apply_on']"):
                node.set('readonly', str(not self.env.company.allow_global_discount_apply_on))
        return arch, view
