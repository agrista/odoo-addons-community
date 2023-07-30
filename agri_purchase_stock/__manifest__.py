# -*- coding: utf-8 -*-
# Part of Contagra. See LICENSE file for full copyright and licensing details.

{
    'name': 'Agri Purchase Stock',
    'summary': 'Agriculture purchase stock module',
    'website': 'https://github.com/agrista/odoo-agri',
    'category': 'Operations/Inventory',
    'version': '0.1.0',
    'sequence': 1,
    'author': 'Contagra',
    'license': 'Other proprietary',
    'description': 'Agriculture purchase stock module',
    'depends': [
        'agri',
        'purchase_stock',
        'uom',
    ],
    'data': [
        'data/uom_data.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
}
