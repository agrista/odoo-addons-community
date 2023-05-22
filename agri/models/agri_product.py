from odoo import fields, models, _


class AgriProduct(models.Model):
    _name = 'agri.product'
    _inherits = {'product.template': 'product_template_id'}
    _description = 'Agri Product'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    product_template_id = fields.Many2one('product.template', string='Product Template', required=True, auto_join=True,
                                          ondelete='cascade', index=True, copy=False, )
    agri_type = fields.Selection([
        ('cultivar', 'Cultivar'),
        ('fertilizer', 'Fertilizer'),
        ('agrochemical', 'Agrochemical'),
    ],
        string='Fertiliser Grading',
        default='cultivar'
    )
    is_agri = fields.Boolean(related='categ_id.is_agri', string='Is Agri',
                             store=True)
    status = fields.Selection([('draft', 'Draft'),
                               ('pending', 'Pending'),
                               ('approved', 'Approved'),
                               ('rejected', 'Rejected')],
                              string="Status",
                              default="draft",
                              copy=False,
                              tracking=True)
    is_cultivar = fields.Boolean('Is Cultivar', default=False)
    leaves_per_plant = fields.Integer('Leaves Per Plant', default=22)

    is_agrochemical = fields.Boolean('Is Agrochemical', default=False)
    active_ingredient_ids = fields.Many2many('agri.active.ingredient',
                                             string='Active Ingredients', )
    pest_disease_ids = fields.Many2many('agri.pest.disease',
                                        string='Pests/Diseases', )
    related_product_category_ids = fields.Many2many('product.category',
                                                    string='Related Categories', )

    is_fertiliser = fields.Boolean('Is Fertiliser', default=False)
    fertiliser_grading_type = fields.Selection(
        [
            ('percentage', 'Percentage'),
            ('oxide', 'Oxide'),
        ],
        string='Fertiliser Grading',
        default='percentage'
    )
    nitrogen = fields.Integer('Nitrogen', default=0)
    phosphorus = fields.Integer('Phosphorus', default=0)
    potassium = fields.Integer('Potassium', default=0)
    nutrient_concentration = fields.Float('Nutrient Concentration', default=0)
    nutrient_concentration_ids = fields.One2many('agri.nutrient.concentration', 'product_id',
                                                 string='Nutrients', copy=True, )

    def action_open_label_layout(self):
        action = self.env['ir.actions.act_window']._for_xml_id('product.action_open_label_layout')
        action['context'] = {'default_product_tmpl_ids': self.ids}
        return action

    def open_pricelist_rules(self):
        self.ensure_one()
        domain = ['|',
            ('product_tmpl_id', '=', self.id),
            ('product_id', 'in', self.product_variant_ids.ids)]
        return {
            'name': _('Price Rules'),
            'view_mode': 'tree,form',
            'views': [(self.env.ref('product.product_pricelist_item_tree_view_from_product').id, 'tree'), (False, 'form')],
            'res_model': 'product.pricelist.item',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': domain,
            'context': {
                'default_product_tmpl_id': self.id,
                'default_applied_on': '1_product',
                'product_without_variants': self.product_variant_count == 1,
            },
        }
