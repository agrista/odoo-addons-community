from odoo import fields, models


class ActiveIngredient(models.Model):
    _name = 'agri.active.ingredient'
    _description = 'Active Ingredient'
    _order = 'name asc'

    name = fields.Char('Name', required=True)

