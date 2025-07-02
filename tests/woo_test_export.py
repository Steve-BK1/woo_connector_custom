# -*- coding: utf-8 -*-
from odoo import models, api
import requests
import logging

_logger = logging.getLogger(__name__)

class WooTestExport(models.TransientModel):
    _name = 'woo.test.export'
    _description = 'Test Export WooCommerce'

    @api.multi
    def test_export_product_to_woocommerce(self):
        # Paramètres de test
        consumer_key = 'ck_a90b66f3bb01196501b88e21eb8468378b35573d'
        consumer_secret = 'cs_33c6e05861e7016916aaa63bafe6f56cb2c53ffa'
        store_url = 'http://localhost/wordpress/?post_type=product'

        # Exemple de données produit
        product_data = {
            "name": "Produit Test Export API",
            "type": "simple",
            "regular_price": "19.99",
            "description": "Ceci est un produit test exporté via l'API WooCommerce depuis Odoo.",
            "short_description": "Produit test",
            "categories": [{"id": 9}],  # adapte selon ta boutique
            "images": [{"src": "https://via.placeholder.com/300"}]
        }

        # URL endpoint WooCommerce REST API
        endpoint = f"{store_url}/wp-json/wc/v3/products"

        try:
            response = requests.post(
                endpoint,
                auth=(consumer_key, consumer_secret),
                json=product_data,
                timeout=20
            )

            if response.status_code in [200, 201]:
                _logger.info("[TEST EXPORT] Produit exporté avec succès vers WooCommerce. Réponse : %s", response.json())
            else:
                _logger.error("[TEST EXPORT] Échec de l'export du produit. Code : %s, Réponse : %s", response.status_code, response.text)

        except Exception as e:
            _logger.error("[TEST EXPORT] Exception lors de l'export WooCommerce : %s", str(e))

        return True
