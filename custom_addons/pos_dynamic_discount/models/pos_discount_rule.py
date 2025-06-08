from odoo import fields, models

class PosDiscountRule(models.Model):
    _name = 'pos.discount.rule'
    _description = 'POS Discount Rule'

    name = fields.Char(string='Rule Name', required=True)
    start_time = fields.Float(string='Start Time (24h)', required=True, help='Enter time in 24-hour format (e.g., 14.0 for 2:00 PM)')
    end_time = fields.Float(string='End Time (24h)', required=True, help='Enter time in 24-hour format (e.g., 17.0 for 5:00 PM)')
    day_of_week = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], string='Day of Week', required=True)
    discount_percentage = fields.Float(string='Discount (%)', required=True, default=10.0)
    pos_config_id = fields.Many2one('pos.config', string='POS Configuration', required=True)