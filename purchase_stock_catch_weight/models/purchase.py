from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    catch_weight_qty = fields.Float(string='Catch Weight', digits=(10, 4))


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _prepare_stock_move_vals(self, picking, price_unit, product_uom_qty, product_uom):
        vals = super(PurchaseOrderLine, self)._prepare_stock_move_vals(picking, price_unit, product_uom_qty, product_uom)
        if self.order_id.catch_weight_qty:
            vals['product_uom_qty'] = self.order_id.catch_weight_qty
        return vals
