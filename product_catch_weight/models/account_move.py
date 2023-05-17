from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    catch_weight = fields.Float(string='Catch Weight', digits=(10, 4), compute='_compute_price', store=True)
    catch_weight_uom_id = fields.Many2one('uom.uom', related='product_id.catch_weight_uom_id')

    @api.depends('price_unit', 'discount', 'tax_ids', 'quantity',
                 'product_id', 'move_id.partner_id', 'move_id.currency_id', 'move_id.company_id',
                 'move_id.invoice_date', 'move_id.date')
    def _compute_price(self):
        currency = self.move_id and self.move_id.currency_id or None
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)

        ratio = 1.0
        qty_done_total = 0.0
        catch_weight = 0.0
        if self.move_id.type in ('out_invoice', 'out_refund'):
            move_lines = self.sale_line_ids.mapped('move_ids.move_line_ids')
        else:
            move_lines = self.purchase_line_id.mapped('move_ids.move_line_ids')
        for move_line in move_lines.filtered(lambda l: l.lot_id):
            qty_done = move_line.qty_done
            current_qty_done = qty_done + qty_done_total
            r = move_line.lot_id.catch_weight_ratio
            if current_qty_done == 0:
                ratio = 0
            else:
                ratio = ((ratio * qty_done_total) + (qty_done * r)) / current_qty_done
            qty_done_total += qty_done
            catch_weight += move_line.lot_id.catch_weight
        price = price * ratio
        self.catch_weight = catch_weight

        taxes = False
        if self.tax_ids:
            taxes = self.tax_ids.compute_all(price, currency, self.quantity, product=self.product_id,
                                                          partner=self.move_id.partner_id)
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else self.quantity * price
        self.price_total = taxes['total_included'] if taxes else self.price_subtotal
        if self.move_id.currency_id and self.move_id.currency_id != self.move_id.company_id.currency_id:
            price_subtotal_signed = self.move_id.currency_id.with_context(
                date=self.move_id._get_currency_rate_date()).compute(price_subtotal_signed,
                                                                        self.move_id.company_id.currency_id)
        sign = self.move_id.move_type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign
