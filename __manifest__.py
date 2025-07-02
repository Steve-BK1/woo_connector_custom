{
    'name': 'WooCommerce Connector Custom',
    'version': '1.0',
    'author': 'Steve BK',
    'summary': 'Connexion de base entre Odoo 11(Jarvis) et WooCommerce via REST API',
    'category': 'E-commerce',
    'website': 'http://www.wise.cm',
    'depends': ['base','product'],
    'data': [
        'views/woo_instance_view.xml',
        'views/product_template_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}