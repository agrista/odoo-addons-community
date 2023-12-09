# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Stock multi-company",
    "summary": "Select individually the stock visibility on each company",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["base_multi_company", "stock"],
    "author": "Agrista",
    "website": "https://github.com/agrista/odoo-multi-company",
    'category': 'Inventory/Inventory',
    "data": ["views/stock_lot_views.xml"],
    "installable": True,
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}
