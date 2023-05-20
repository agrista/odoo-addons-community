# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    lot_catch_weight_ratio = fields.Float(related='lot_id.catch_weight_ratio')
    lot_catch_weight = fields.Float(related='lot_id.catch_weight')
    lot_catch_weight_uom_id = fields.Many2one('uom.uom', related='lot_id.catch_weight_uom_id')
