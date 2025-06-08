# inventory_expiry_notification/models/stock_lot.py
from odoo import models, fields
from datetime import datetime, timedelta
from odoo.tools import format_date

class StockLot(models.Model):
    _inherit = 'stock.lot'

    def _check_expiry(self):
        """Check lots nearing expiration and send notifications."""
        # Cari lot dengan tanggal kadaluarsa dalam 7 hari
        expiry_threshold = datetime.now() + timedelta(days=7)
        lots = self.env['stock.lot'].search([
            ('expiration_date', '!=', False),
            ('expiration_date', '<=', expiry_threshold),
            ('product_qty', '>', 0),  # Hanya lot dengan stok > 0
        ])

        for lot in lots:
            product = lot.product_id
            expiry_date = fields.Datetime.to_string(lot.expiration_date)
            message = (
                f"Warning: Lot {lot.name} for product {product.name} "
                f"is nearing expiration on {format_date(self.env, expiry_date)}."
            )
            # Buat notifikasi di produk
            product.message_post(
                body=message,
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
            )

            # (Opsional) Kirim email ke manajer stok
            if lot.company_id.stock_manager_id:
                template = self.env.ref('inventory_expiry_notification.email_template_expiry')
                template.send_mail(
                    lot.id,
                    force_send=True,
                    email_values={
                        'recipient_ids': [(4, lot.company_id.stock_manager_id.partner_id.id)],
                    }
                )