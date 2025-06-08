{
    'name': 'PoS QRCode Camera Integration',
    'version': '1.0',
    'category': 'Point of Sale',
    'depends': ['point_of_sale'],  # Depends on the PoS module
    'data': [
        # Add views or data files if needed (e.g., for backend config)
    ],
    'qweb': ['static/src/xml/qr_scanner.xml'],  # QWeb templates for PoS frontend
    'assets': {
        'point_of_sale.assets': [
            'pos_qrcode_camera/static/lib/html5-qrcode.min.js',
            'pos_qrcode_camera/static/src/js/qr_scanner.js',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}