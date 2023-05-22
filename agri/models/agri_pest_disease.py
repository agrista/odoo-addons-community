from odoo import fields, models


class PestDisease(models.Model):
    _name = 'agri.pest.disease'
    _description = 'Pest & Disease'
    _order = 'name asc'

    name = fields.Char('Name', required=True)
    scientific_name = fields.Char('Scientific Name', required=False)

