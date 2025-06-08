{
    'name': 'POS Auto Print Receipt',
    'version': '1.0',
    'depends': ['point_of_sale'],
    'author': 'oneframe',
    'category': 'Point of Sale',
    'summary': 'Automatically print POS receipt after payment',
    'description': 'Adds an option to automatically print receipt upon payment validation in POS.',
    'data': [
        'views/pos_config_view.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_auto_print/static/src/js/receipt_auto_print.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
