{
    'name': 'Odoo Hosting',
    'version': '1.0',
    'description': 'Odoo Hosting',
    'category': 'Website',
    'depends': ['website','crm','mail'],
    'data': [
        'data/crm_tags.xml',
        'views/template.xml',
        'views/menu.xml',
        'views/email_verification.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'odoo_hosting_page/static/src/css/hosting_style.css',
            'odoo_hosting_page/static/src/js/otp.js',
        ],
    },
    'license' : 'LGPL-3',
    'installable': True,
    'application': True,
}