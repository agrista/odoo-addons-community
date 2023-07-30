from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    agri_atlas_uri = fields.Char(
        string="Atlas URI",
        help="Contagra Atlas URI for point-in-polygon requests",
        config_parameter="agri.atlas_uri",
        default="https://atlas.agrista.com",
    )
