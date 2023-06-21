{
    'name': 'Stock Attribute Set',
    'version': '1.1.0',
    'category': 'Generic Modules/Others',
    'license': 'Other proprietary',
    'author': 'Agrista',
    'website': 'https://github.com/agrista/odoo-agri',
    'depends': ['stock', 'product_attribute_set'],
    'data': [
        # 'views/product_attribute_group.xml',
        'views/product_category.xml',
        'views/stock_lot_views.xml',
        'views/product.xml',
        'views/stock_lot_views.xml',
        'views/stock_move_line_attribute_attribute.xml',
        'views/stock_move_line_attribute_group.xml',
        'views/stock_move_line_attribute_set.xml',
        'views/stock_move_line_views.xml'
    ],
    'installable': True,
}
