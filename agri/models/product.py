from odoo import fields, models


class ProductTemplate(models.Model):
    _name = 'product.template'
    _description = 'Product Template'
    _inherit = ['product.template']

    is_agri = fields.Boolean(related='categ_id.is_agri', string='Is Agri',
                             store=True)
