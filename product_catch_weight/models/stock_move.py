# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_catch_weight_uom_id = fields.Many2one('uom.uom', related="product_id.catch_weight_uom_id")

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        vals = super(StockMove, self)._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant)
        vals['catch_weight_uom_id'] = self.product_catch_weight_uom_id.id if self.product_catch_weight_uom_id else False
        return vals

    def action_show_details(self):
        action = super(StockMove, self).action_show_details()
        action['context']['show_catch_weight'] = bool(self.product_id.catch_weight_uom_id)
        return action

