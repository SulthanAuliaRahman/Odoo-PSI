{
    'name': 'POS Dynamic Discount Rules',
    'version': '1.0',
    'category': 'Point of Sale',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_templates.xml',
        'views/pos_discount_rule_views.xml',  # Add this line
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_dynamic_discount/static/src/js/pos_dynamic_discount.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}