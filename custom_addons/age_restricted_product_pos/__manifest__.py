{
    'name': 'POS Age Restricted Products',
    'version': '17.0.1.0.0',
    'summary': 'This Module will help to restrict the age restricted products '
               'in pos.',
    'description': 'Modul untuk membatasi pembelian suatu barang'
                   ' agar tidak sembarang orang dapat membeli barang tertentu'
                   ' memberikan batasan umur pada suatu barang'
                   'sehingga menampilkan popup untuk informasi bahwa terdapat minimum umur untuk pembelian barang tertentu',
    'category': 'Point of Sale',
    'author': 'Afriza',
    'company': 'Alfamart',
    'depends': ['base', 'point_of_sale', 'product'],
    'data': [
        'views/age_restrict_product_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'age_restricted_product_pos/static/src/js/age_restrict.js',
            'age_restricted_product_pos/static/src/js/restrict_popup.js',
            'age_restricted_product_pos/static/src/xml/restrict_popup.xml',
        ],
    },
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
