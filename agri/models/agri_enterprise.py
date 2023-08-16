from odoo import api, fields, models


class Enterprise(models.Model):
    _name = 'agri.enterprise'
    _description = 'Enterprise'
    _order = 'name asc'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    type = fields.Selection([('crop', 'Crop'),
                             ('permanent_crop', 'Permanent Crop'),
                             ('livestock', 'Livestock')],
                            string='Type',
                            default='crop',
                            required=True)
    # Cycles are relevant for permanent crops, indicate the year from
    # establishment. Starts with one.
    cycles = fields.Integer('Cycles', default=1,
                           help='Cycles are relevant for permanent crops, indicate the year from establishment.')
    calendar_period_type = fields.Many2one('date.range.type',
                                           string='Calendar Period Type',
                                           domain="[('is_calendar_period', '=', True)]",
                                           required=True)
    # The season is specified units defined by the calendar period type
    season_start = fields.Integer('Season Start', required=True)
    season_end = fields.Integer('Season End', required=True)
    line_ids = fields.One2many('agri.enterprise.line',
                               'enterprise_id',
                               'Lines',
                               copy=True)
    stage_ids = fields.One2many('agri.enterprise.stage',
                                'enterprise_id',
                                'Stages',
                                copy=True)


class EnterpriseLine(models.Model):
    _name = 'agri.enterprise.line'
    _description = 'Enterprise Line'

    enterprise_id = fields.Many2one('agri.enterprise',
                                    'Enterprise',
                                    required=True)
    product_category_id = fields.Many2one('product.category',
                                          'Category',
                                          domain="[('is_agri', '=', True)]",
                                          required=True)
    cost_type = fields.Selection(related='product_category_id.cost_type',
                                 readonly=True)
    sale_ok = fields.Boolean(related='product_category_id.sale_ok',
                             readonly=True)
    purchase_ok = fields.Boolean(related='product_category_id.purchase_ok',
                                 readonly=True)


class EnterpriseStage(models.Model):
    _name = 'agri.enterprise.stage'
    _description = 'Enterprise Stage'
    _order = 'sequence,name'

    name = fields.Char()
    sequence = fields.Integer()
    enterprise_id = fields.Many2one('agri.enterprise',
                                    'Enterprise',
                                    required=True)
    stage_start = fields.Integer('Stage Start')
    stage_end = fields.Integer('Stage End')
    fold = fields.Boolean()
    enterprise_state = fields.Selection([('planned', 'Planned'),
                                         ('inprogress', 'In Progress'),
                                         ('done', 'Done')],
                                        'State',
                                        default="planned")
