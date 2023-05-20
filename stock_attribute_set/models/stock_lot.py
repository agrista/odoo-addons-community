# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockLot(models.Model):
    """The mixin 'attribute.set.owner.mixin' override the model's fields_view_get()
    method which will replace the 'attributes_placeholder' by a group made up of all
    the product.template's Attributes.
    Each Attribute will have a conditional invisibility depending on its Attriute Sets.
    """

    _inherit = ["stock.lot", "attribute.set.owner.mixin"]
    _name = "stock.lot"

    attribute_set_id = fields.Many2one(
        "attribute.set",
        "Attribute Set",
    )

    @api.model
    def create(self, vals):
        if not vals.get("attribute_set_id") and vals.get("product_id"):
            product = self.env["product.product"].browse(vals["product_id"])
            vals["attribute_set_id"] = product.stock_attribute_set_id.id
        return super().create(vals)

    def write(self, vals):
        if not vals.get("attribute_set_id") and vals.get("product_id"):
            product = self.env["product.product"].browse(vals["product_id"])
            vals["attribute_set_id"] = product.stock_attribute_set_id.id
        return super().write(vals)

    @api.onchange("product_id")
    def update_att_set_onchange_product_id(self):
        self.ensure_one()
        if self.product_id and not self.attribute_set_id:
            self.attribute_set_id = self.product_id.stock_attribute_set_id
