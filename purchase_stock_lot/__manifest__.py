{
    'name': 'Purchase Stock Lot',
    'version': '1.0.0',
    'category': 'Warehouse',
    'depends': [
        'base',
        'stock',
        'purchase',
        'purchase_stock',
    ],
    'description': """
    Show lots/serial numers assocaited with a purchase order.
    """,
    'author': 'Contagra',
    'license': 'AGPL-3',
    'website': 'https://agrista.com/',
    'data': [
        'views/purchase_views.xml',
    ],
    'installable': True,
    'application': False,
}
