from odoo import fields, models


class Nutrient(models.Model):
    _name = 'agri.nutrient'
    _description = 'Nutrient'
    _order = 'name asc'

    name = fields.Char('Name', required=True)
    element = fields.Char('Element')


class NutrientConcentration(models.Model):
    _name = 'agri.nutrient.concentration'
    _description = 'Nutrient Concentration'
    _order = 'concentration_perc asc'

    product_id = fields.Many2one('product.template', required=True)
    nutrient_id = fields.Many2one('agri.nutrient', required=True)
    concentration_perc = fields.Float('')
