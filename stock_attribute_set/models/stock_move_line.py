# Copyright 2011 Akretion (http://www.akretion.com).
# @author Benoit Guillot <benoit.guillot@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class StockMoveLine(models.Model):
    """The mixin 'attribute.set.owner.mixin' override the model's fields_view_get()
    method which will replace the 'attributes_placeholder' by a group made up of all
    the product.template's Attributes.
    Each Attribute will have a conditional invisibility depending on its Attribute Sets.
    """

    _inherit = ["stock.move.line"]
    _name = "stock.move.line"

    attribute_set_id = fields.Many2one('attribute.set', 'Attribute Set', related='lot_id.attribute_set_id', store=True,
                                       readonly=True)
