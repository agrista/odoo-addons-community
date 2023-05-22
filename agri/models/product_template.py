from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_agri = fields.Boolean(related='categ_id.is_agri',
                             store=True)
    is_cultivar = fields.Boolean('Is Cultivar', default=False)
    leaves_per_plant = fields.Integer('Leaves Per Plant', default=22)

    is_agrochemical = fields.Boolean('Is Agrochemical', default=False)
    active_ingredient_ids = fields.Many2many('agri.active.ingredient',
                                             string='Active Ingredients', )
    pest_disease_ids = fields.Many2many('agri.pest.disease',
                                        string='Pests/Diseases', )
    related_product_category_ids = fields.Many2many('product.category',
                                                    string='Related Categories', )

    is_fertiliser = fields.Boolean('Is Fertiliser', default=False)
    fertiliser_grading_type = fields.Selection(
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
