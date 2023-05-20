# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    has_catch_weight = fields.Boolean(string="Has Catch Weight", compute='_compute_has_catch_weight', store=True)

    @api.depends('move_ids.product_catch_weight_uom_id')
    def _compute_has_catch_weight(self):
        for picking in self:
            picking.has_catch_weight = any(picking.mapped('move_ids.product_catch_weight_uom_id'))
