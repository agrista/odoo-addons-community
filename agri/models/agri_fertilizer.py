from odoo import fields, models, _


class AgriFertilizer(models.Model):
    _name = 'agri.fertilizer'
    _description = 'Agri Fertilizer'
    _inherits = {'product.template': 'product_tmpl_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']

    product_tmpl_id = fields.Many2one('product.template', string='Product Template', required=True, auto_join=True,
                                          ondelete='cascade', index=True, copy=False, )
    fertilizer_grading_type = fields.Selection(
        [
            ('percentage', 'Percentage'),
            ('oxide', 'Oxide'),
        ],
        string='Fertiliser Grading',
        default='percentage'
    )
    nitrogen = fields.Integer('Nitrogen', default=0)
    phosphorus = fields.Integer('Phosphorus', default=0)
    potassium = fields.Integer('Potassium', default=0)
    nutrient_concentration = fields.Float('Nutrient Concentration', default=0)
    nutrient_concentration_ids = fields.One2many('agri.nutrient.concentration', 'product_id',
                                                 string='Nutrients', copy=True, )

