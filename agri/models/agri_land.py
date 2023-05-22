from odoo import fields, models


class LandUse(models.Model):
    _name = 'agri.land.use'
    _description = 'Land Use'
    _order = 'name asc'

    class_id = fields.Integer('Class', required=True)
    name = fields.Char('Name', required=True)
    irrigated = fields.Boolean('Irrigated', default=False)
