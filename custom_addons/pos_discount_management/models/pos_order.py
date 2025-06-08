from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    total_discount = fields.Float(string="Total Discount", compute="_compute_total_discount")

    @api.depends('lines', 'lines.discount')
    def _compute_total_discount(self):
        for rec in self:
            total_discount = 0
            for line in rec.lines.filtered(lambda l: l.discount):
                currency_rate = line.order_id.currency_rate
                total_discount += ((line.qty * line.price_unit) * (
                            line.discount / 100)) / currency_rate if currency_rate else 1
            rec.total_discount = total_discount
