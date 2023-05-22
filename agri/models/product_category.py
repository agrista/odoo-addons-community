from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductCategory(models.Model):
    _inherit = 'product.category'

    is_agri = fields.Boolean('Is Agri', default=False)
    cost_type = fields.Selection(
        [
            ('crop_establishment', 'Crop Establishment'),
            ('crop_input', 'Crop Input'),
            ('crop_harvest', 'Crop Harvest'),
            ('crop_marketing', 'Crop Marketing'),
            ('crop', 'Crop'),
            ('permanent_crop', 'Permanent Crop'),
            ('grazing', 'Grazing'),
            ('livestock', 'Livestock'),
            ('animal_feed', 'Animal Feed'),
            ('husbandry', 'Husbandry'),
            ('livestock_harvest', 'Livestock Harvest'),
            ('livestock_product', 'Livestock Product'),
            ('timber', 'Timber'),
            ('overhead', 'Overhead'),
            ('non_agri', 'Non Agri'),
            ('other', 'Other'),
        ],
        string='Cost Type',
        default=False
    )
    cost_driver = fields.Selection(
        [
            ('land', 'Land'),
            ('crop', 'Crop'),
            ('transport', 'Transport'),
            ('herd', 'Herd'),
            ('head', 'Head'),
            ('overhead', 'Overhead'),
        ],
        string='Cost Driver'
    )
    uom_id = fields.Many2one(
        'uom.uom',
        'Default UoM',
        help='Default unit of measure used for allocating costs.'
    )
    sale_ok = fields.Boolean('Can be Sold', default=False)
    purchase_ok = fields.Boolean('Can be Purchased', default=False)

    @api.constrains('cost_type')
    def _check_cost_type(self):
        for category in self:
            if category.is_agri and not category.cost_type:
                raise ValidationError(_('Cost Type must be set agricultural product categories'))

    @api.constrains('uom_id')
    def _check_uom_id(self):
        for category in self:
            if category.is_agri and not category.uom_id:
                raise ValidationError(_('Unit of Measure must be set agricultural product categories'))

    @api.constrains('cost_type')
    def _check_cost_type(self):
        for category in self:
            if category.is_agri and not category.cost_type:
                raise ValidationError(_('The cost type must be set for agricultural product categories'))
