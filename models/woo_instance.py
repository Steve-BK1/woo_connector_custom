from odoo import models, fields, api
from odoo.exceptions import UserError
import requests

class WooInstance(models.Model):
    _name = 'woo.instance'
    _description = 'Instance WooCommerce'

    name = fields.Char(string="Nom de la boutique", required=True)
    url = fields.Char(string="URL WooCommerce", required=True)
    consumer_key = fields.Char(string="Consumer Key", required=True)
    consumer_secret = fields.Char(string="Consumer Secret", required=True)
    is_connected = fields.Boolean(string="Connecté", compute="_check_connection", store=True)

    @api.depends('url', 'consumer_key', 'consumer_secret')
    def _check_connection(self):
        for record in self:
            record.is_connected = record._test_connection()

    def _test_connection(self):
        """ Méthode interne pour tester la connexion """
        try:
            response = requests.get(
                f"{self.url}/wp-json/wc/v3/",
                auth=(self.consumer_key, self.consumer_secret),
                timeout=10
            )
            return response.status_code == 200
        except Exception:
            return False

    @api.multi
    def button_test_connection(self):
        """ Bouton pour tester manuellement la connexion """
        self.ensure_one()
        connected = self._test_connection()
        self.is_connected = connected
        if connected:
            # ⚠ Odoo 11 ne supporte pas display_notification !
            raise UserError("🎉 Connexion réussie à WooCommerce !")
        else:
            raise UserError("⚠ Connexion échouée ! Vérifie l'URL, la clé ou le secret.")
