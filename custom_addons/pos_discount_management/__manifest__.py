{
    'name': "POS Discount Management",

    'summary': """POS Discount Management""",
    'description': """ This APP Manage Discount on POS Session (order - line) Fixed or Percentage.""",

    'category': 'Adevx/retail',
    'author': 'Adevx',
    'license': "OPL-1",
    'website': 'https://adevx.com',
    "price": 0,
    "currency": 'USD',

    'depends': ['pos_discount'],
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Views
        'views/pos_global_discount.xml',
        'views/pos_config.xml',
        'views/pos_order.xml',
        'views/res_config_settings.xml',
        'views/menu.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_discount_management/static/src/js/*.js',
        ],
    },
    'images': ['static/description/banner.png'],

    'installable': True,
    'application': True,
    'auto_install': False,
}
