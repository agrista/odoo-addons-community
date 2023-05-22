from odoo import api, fields, models, _


class Country(models.Model):
    _inherit = 'res.country'

    def _update_za_address_format(self):
        country_ids = self.env['res.country'].search([('code', '=', 'ZA')])
        country_ids.write({'address_format': '%(street)s\n%(street2)s\n%(city)s\n%(state_name)s\n%(zip)s\n%(country_name)s'})

    @api.model
    def update_za_address_format(self):
        self._update_za_address_format()
