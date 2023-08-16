from odoo import fields, models, _


class AgriAgrochemical(models.Model):
    _name = 'agri.agrochemical'
    _description = 'Agri Agrochemical'
    _inherits = {'product.template': 'product_tmpl_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']

    product_tmpl_id = fields.Many2one('product.template', string='Product Template', required=True, auto_join=True,
                                          ondelete='cascade', index=True, copy=False, )
    active_ingredient_ids = fields.Many2many('agri.active.ingredient',
                                             string='Active Ingredients', )
    pest_disease_ids = fields.Many2many('agri.pest.disease',
                                        string='Pests/Diseases', )
    related_product_category_ids = fields.Many2many('product.category',
                                                    string='Related Categories', )
