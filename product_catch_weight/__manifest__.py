{
    'name': 'Product Catch Weight',
    'version': '1.0.0',
    'category': 'Warehouse',
    'depends': [
        'sale_stock',
        'purchase',
    ],
    'description': """
    """,
    'author': 'Hibou Corp., Contagra',
    'license': 'LGPL-3',
    'website': 'https://hibou.io/',
    'data': [
        'views/account_move_views.xml',
        'views/product_views.xml',
        'views/stock_views.xml',
    ],
    'installable': True,
    'application': False,
}
