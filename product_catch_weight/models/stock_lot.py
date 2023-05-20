# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockLot(models.Model):
    _inherit = 'stock.lot'

    catch_weight_ratio = fields.Float(string='Catch Weight Ratio', digits=(10, 6), compute='_compute_catch_weight_ratio')
    catch_weight = fields.Float(string='Catch Weight', digits=(10, 4))
    catch_weight_uom_id = fields.Many2one('uom.uom', string='Catch Weight UoM', related='product_id.catch_weight_uom_id')

    @api.depends('catch_weight')
    def _compute_catch_weight_ratio(self):
        for lot in self:
            if not lot.catch_weight_uom_id:
                lot.catch_weight_ratio = 1.0
            else:
                lot.catch_weight_ratio = lot.catch_weight_uom_id._compute_quantity(lot.catch_weight,
                                                                                   lot.product_id.uom_id,
                                                                                   rounding_method='DOWN')