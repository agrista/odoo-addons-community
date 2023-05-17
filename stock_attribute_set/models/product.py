from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    stock_attribute_set_id = fields.Many2one(
        "attribute.set",
        "Stock Attribute Set",
        default=lambda self: self._get_default_stock_att_set(),
    )

    def _get_default_stock_att_set(self):
        """Fill default Product's stock_attribute_set with its
        Category's default stock_attribute_set."""
        default_categ_id_id = self._get_default_category_id()
        if default_categ_id_id:
            default_categ_id = self.env["product.category"].search(
                [("id", "=", default_categ_id_id.id)]
            )
            return default_categ_id.stock_attribute_set_id.id

    @api.model
    def create(self, vals):
        if not vals.get("stock_attribute_set_id") and vals.get("categ_id"):
            category = self.env["product.category"].browse(vals["categ_id"])
            vals["stock_attribute_set_id"] = category.stock_attribute_set_id.id
        return super().create(vals)

    def write(self, vals):
        if not vals.get("stock_attribute_set_id") and vals.get("categ_id"):
            category = self.env["product.category"].browse(vals["categ_id"])
            vals["stock_attribute_set_id"] = category.stock_attribute_set_id.id
        return super().write(vals)

    @api.onchange("categ_id")
    def update_att_set_onchange_categ_id(self):
        self.ensure_one()
        if self.categ_id and not self.attribute_set_id:
            self.attribute_set_id = self.categ_id.attribute_set_id
            self.stock_attribute_set_id = self.categ_id.stock_attribute_set_id
