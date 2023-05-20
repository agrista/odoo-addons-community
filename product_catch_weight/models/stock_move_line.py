# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round, float_compare


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    catch_weight_ratio = fields.Float(string='Catch Weight Ratio', digits=(10, 6), default=1.0)
    catch_weight = fields.Float(string='Catch Weight', digits=(10,4))
    catch_weight_uom_id = fields.Many2one('uom.uom', string='Catch Weight UOM')
    lot_catch_weight = fields.Float(related='lot_id.catch_weight')
    lot_catch_weight_uom_id = fields.Many2one('uom.uom', related='product_id.catch_weight_uom_id')

    def _action_done(self):
        """ This method is called during a move's `action_done`. It'll actually move a quant from
        the source location to the destination location, and unreserve if needed in the source
        location.

        This method is intended to be called on all the move lines of a move. This method is not
        intended to be called when editing a `done` move (that's what the override of `write` here
        is done).
        """

        # First, we loop over all the move lines to do a preliminary check: `qty_done` should not
        # be negative and, according to the presence of a picking type or a linked inventory
        # adjustment, enforce some rules on the `lot_id` field. If `qty_done` is null, we unlink
        # the line. It is mandatory in order to free the reservation and correctly apply
        # `action_done` on the next move lines.
        move_lines_to_delete = self.env['stock.move.line']
        for move_line in self:
            # Check here if `ml.qty_done` respects the rounding of `ml.product_uom_id`.
            uom_qty = float_round(move_line.qty_done, precision_rounding=move_line.product_uom_id.rounding,
                                  rounding_method='HALF-UP')
            precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            qty_done = float_round(move_line.qty_done, precision_digits=precision_digits, rounding_method='HALF-UP')
            if float_compare(uom_qty, qty_done, precision_digits=precision_digits) != 0:
                raise UserError(_('The quantity done for the product "%s" doesn\'t respect the rounding precision \
                                  defined on the unit of measure "%s". Please change the quantity done or the \
                                  rounding precision of your unit of measure.') % (
                    move_line.product_id.display_name, move_line.product_uom_id.name))

            qty_done_float_compared = float_compare(move_line.qty_done, 0,
                                                    precision_rounding=move_line.product_uom_id.rounding)
            if qty_done_float_compared > 0:
                if move_line.product_id.tracking != 'none':
                    picking_type_id = move_line.move_id.picking_type_id
                    if picking_type_id:
                        if picking_type_id.use_create_lots:
                            # If a picking type is linked, we may have to create a production lot on
                            # the fly before assigning it to the move line if the user checked both
                            # `use_create_lots` and `use_existing_lots`.
                            if move_line.lot_name and not move_line.lot_id:
                                lot_catch_weight = move_line.catch_weight_uom_id._compute_quantity(
                                    move_line.catch_weight,
                                    move_line.product_id.catch_weight_uom_id,
                                    rounding_method='DOWN')
                                lot = self.env['stock.lot'].create({
                                    'name': move_line.lot_name,
                                    'product_id': move_line.product_id.id,
                                    'catch_weight': lot_catch_weight,
                                    'company_id': self.company_id.id,
                                })
                                move_line.write({'lot_id': lot.id})
                        elif not picking_type_id.use_create_lots and not picking_type_id.use_existing_lots:
                            # If the user disabled both `use_create_lots` and `use_existing_lots`
                            # checkboxes on the picking type, he's allowed to enter tracked
                            # products without a `lot_id`.
                            continue
                    elif move_line.move_id.is_inventory:
                        # If an inventory adjustment is linked, the user is allowed to enter
                        # tracked products without a `lot_id`.
                        continue

                    if not move_line.lot_id:
                        raise UserError(_('You need to supply a lot/serial number for %s.') % move_line.product_id.name)
            elif qty_done_float_compared < 0:
                raise UserError(_('No negative quantities allowed'))
            else:
                move_lines_to_delete |= move_line
        move_lines_to_delete.unlink()

        # Now, we can actually move the quant.
        move_lines_done = self.env['stock.move.line']
        for move_line in self - move_lines_to_delete:
            if move_line.product_id.type == 'product':
                Quant = self.env['stock.quant']
                rounding = move_line.product_uom_id.rounding

                # if this move line is force assigned, unreserve elsewhere if needed
                if not move_line.location_id.should_bypass_reservation() and float_compare(move_line.qty_done,
                                                                                           move_line.reserved_qty,
                                                                                           precision_rounding=rounding) > 0:
                    extra_qty = move_line.qty_done - move_line.reserved_qty
                    move_line._free_reservation(move_line.product_id, move_line.location_id, extra_qty,
                                                lot_id=move_line.lot_id,
                                                package_id=move_line.package_id, owner_id=move_line.owner_id,
                                                ml_ids_to_ignore=move_lines_done)
                # unreserve what's been reserved
                if not move_line.location_id.should_bypass_reservation() and move_line.product_id.type == 'product' and move_line.reserved_qty:
                    try:
                        Quant._update_reserved_quantity(move_line.product_id, move_line.location_id,
                                                        -move_line.reserved_qty, lot_id=move_line.lot_id,
                                                        package_id=move_line.package_id, owner_id=move_line.owner_id,
                                                        strict=True)
                    except UserError:
                        Quant._update_reserved_quantity(move_line.product_id, move_line.location_id,
                                                        -move_line.reserved_qty, lot_id=False,
                                                        package_id=move_line.package_id, owner_id=move_line.owner_id,
                                                        strict=True)

                # move what's been actually done
                quantity = move_line.product_uom_id._compute_quantity(move_line.qty_done,
                                                                      move_line.move_id.product_id.uom_id,
                                                                      rounding_method='HALF-UP')
                available_qty, in_date = Quant._update_available_quantity(move_line.product_id, move_line.location_id,
                                                                          -quantity,
                                                                          lot_id=move_line.lot_id,
                                                                          package_id=move_line.package_id,
                                                                          owner_id=move_line.owner_id)
                if available_qty < 0 and move_line.lot_id:
                    # see if we can compensate the negative quants with some untracked quants
                    untracked_qty = Quant._get_available_quantity(move_line.product_id, move_line.location_id,
                                                                  lot_id=False,
                                                                  package_id=move_line.package_id,
                                                                  owner_id=move_line.owner_id,
                                                                  strict=True)
                    if untracked_qty:
                        taken_from_untracked_qty = min(untracked_qty, abs(quantity))
                        Quant._update_available_quantity(move_line.product_id, move_line.location_id,
                                                         -taken_from_untracked_qty,
                                                         lot_id=False, package_id=move_line.package_id,
                                                         owner_id=move_line.owner_id)
                        Quant._update_available_quantity(move_line.product_id, move_line.location_id,
                                                         taken_from_untracked_qty,
                                                         lot_id=move_line.lot_id, package_id=move_line.package_id,
                                                         owner_id=move_line.owner_id)
                Quant._update_available_quantity(move_line.product_id, move_line.location_dest_id, quantity,
                                                 lot_id=move_line.lot_id,
                                                 package_id=move_line.result_package_id, owner_id=move_line.owner_id,
                                                 in_date=in_date)
            move_lines_done |= move_line
        # Reset the reserved quantity as we just moved it to the destination location.
        (self - move_lines_to_delete).with_context(bypass_reservation_update=True).write({
            'reserved_uom_qty': 0.00,
            'date': fields.Datetime.now(),
        })
