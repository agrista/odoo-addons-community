from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _compute_qty_received(self):
        variable_lines = self.env['purchase.order.line']
        stock_lines = self.filtered(lambda order_line: order_line.qty_received_method == 'stock_moves')
        for stock_line in stock_lines:
            if stock_line.product_uom.is_variable_weight:
                variable_lines += stock_line
        super(PurchaseOrderLine, self - variable_lines)._compute_qty_received()
        for variable_line in variable_lines:
            total = 0.0
            for move in variable_line._get_po_line_moves():
                if move.state == 'done':
                    if move._is_purchase_return():
                        if move.to_refund:
                             total -= variable_line.product_qty
                    elif move.origin_returned_move_id and move.origin_returned_move_id._is_dropshipped() and not move._is_dropshipped_returned():
                        pass
                    else:
                        total += variable_line.product_qty
            variable_line._track_qty_received(total)
            variable_line.qty_received = total
