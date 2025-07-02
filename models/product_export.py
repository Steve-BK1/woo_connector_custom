from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    woo_product_id = fields.Char(string='WooCommerce Product ID')

    def export_to_woocommerce(self):
        _logger.debug(" Début de la méthode export_to_woocommerce")

        instance = self.env['woo.instance'].search([], limit=1)
        if not instance:
            _logger.error(" Aucune instance WooCommerce trouvée")
            raise UserError("Aucune instance WooCommerce configurée.")

        _logger.debug(" Instance WooCommerce trouvée : %s", instance)

        for product in self:
            _logger.debug(" Préparation du produit '%s' pour l'export", product.name)

            data = {
                "name": product.name,
                "type": "simple",
                "regular_price": str(product.list_price),
                "description": product.description_sale or "",
                "manage_stock": True,
                "stock_quantity": int(product.qty_available),
                "sku": product.default_code or "",
            }

            _logger.debug(" Données préparées pour l'envoi : %s", data)

            try:
                response = requests.post(
                    f"{instance.url}/wp-json/wc/v3/products",
                    auth=(instance.consumer_key, instance.consumer_secret),
                    json=data
                )

                _logger.debug(" Requête POST envoyée à WooCommerce")
                _logger.debug(" Réponse reçue : %s", response.text)

                if response.status_code == 201:
                    woo_product = response.json()
                    product.woo_product_id = woo_product['id']
                    _logger.info(" Produit '%s' exporté avec succès vers WooCommerce (ID : %s)", product.name,
                                 woo_product['id'])
                else:
                    _logger.error(" Erreur d'export : %s", response.text)
                    raise UserError(f"Erreur lors de l'export : {response.text}")

            except Exception as e:
                safe_name = product.name.encode('ascii', 'ignore').decode()
                _logger.error(" Exception lors de l'export du produit '%s'", product.name, exc_info=True)
                raise UserError(f"Erreur inattendue lors de l'export : {str(e)}")
