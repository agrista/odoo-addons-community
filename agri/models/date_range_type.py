from odoo import models, fields, api, _
from odoo.exceptions import UserError


class DateRangeType(models.Model):
    _inherit = "date.range.type"

    is_calendar_period = fields.Boolean(string='Is Calendar Period',
                                        default=False)
    calendar_period_type = fields.Selection([
        ('week', 'Week'),
        ('month', 'Month'),
    ], string='Calendar Period Type')
    is_allocation_period = fields.Boolean(string='Is Allocation Period', default=False)
    allocation_period_type = fields.Selection([
        ('season', 'Season'),
        ('activity', 'Activity'),
        ('slot', 'Delivery Slot'),
    ], string='Allocation Period Type')
    # TODO: Add constraints per period type

    def unlink(self):
        for rec in self:
            if (rec.is_calendar_period or
                rec.is_allocation_period) and not self._context.get('force_delete'):
                raise UserError(
                    _('You cannot delete a date range type with '
                      'flag "is_calendar_period" or "is_allocation_period"'))
        return super(DateRangeType, self).unlink()
