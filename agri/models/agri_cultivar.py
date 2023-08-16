from odoo import fields, models


class AgriCultivar(models.Model):
    _name = 'agri.cultivar'
    _description = 'Agri Cultivar'
    _inherits = {'product.template': 'product_tmpl_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']

    product_tmpl_id = fields.Many2one('product.template', string='Product Template', required=True, auto_join=True,
                                 ondelete='cascade', index=True, copy=False, )
    leaves_per_plant = fields.Integer('Leaves Per Plant', default=22)
