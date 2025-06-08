# inventory_expiry_notification/__manifest__.py
{
    'name': 'Inventory Expiry Notification',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Notify users about products nearing expiration',
    'depends': ['stock', 'mail'],  # 'stock' untuk Inventory, 'mail' untuk notifikasi
    'data': [
        'data/cron.xml',
        'data/email_template.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}