# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    stock_lot_ids = fields.Many2many('stock.lot', compute='_compute_stock_lot_ids', string='Lots', copy=False,
                                    readonly=True, store=False)
    stock_lot_count = fields.Integer(string='Stock Lot Count', compute='_compute_stock_lot_ids')

    @api.depends('order_line.move_ids.picking_id')
    def _compute_stock_lot_ids(self):
        for order in self:
            stock_moves = self.env['stock.move.line'].search([
                ('move_id.purchase_line_id', '=', order.id),
                ('state', '=', 'done')
            ]).mapped('move_id')
            stock_moves = stock_moves.search([('id', 'in', stock_moves.ids)]).filtered(
                lambda move: move.picking_id.location_id.usage == 'supplier' and move.state == 'done')
            order.stock_lot_ids = stock_moves.mapped('move_line_ids.lot_id')
            order.stock_lot_count = len(order.stock_lot_ids)

    def action_open_purchase_stock_lot(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_production_lot_form")
        action['domain'] = [('purchase_order_ids', 'in', self.id)]
        action['context'] = {
            'default_product_id': self.id,
            'set_product_readonly': True,
            'default_company_id': (self.company_id or self.env.company).id,
        }
        return action
