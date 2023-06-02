from odoo import fields, models


class UoM(models.Model):
    _inherit = 'uom.uom'

    is_variable_weight = fields.Boolean('Is Variable Weight', default=False)
