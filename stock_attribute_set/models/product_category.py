from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    stock_attribute_set_id = fields.Many2one(
        "attribute.set",
        "Default Stock Attribute Set",
        context={"default_model_id": "stock.move.line"},
    )

    def write(self, vals):
        """Fill Category's products with Category's default stock_attribute_set_id if empty"""
        super().write(vals)
        for record in self:
            if vals.get("lot_attribute_set_id"):
                product_ids = self.env["product.template"].search(
                    [("categ_id", "=", record.id), ("stock_attribute_set_id", "=", False)]
                )
                for product_id in product_ids:
                    product_id.stock_attribute_set_id = record.stock_attribute_set_id
        return True
