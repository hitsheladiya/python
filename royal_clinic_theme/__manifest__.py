{
    'name': 'Royal Clinic Theme',
    'version': '1.0',
    'summary': 'Custom website theme for Royal Clinic based on Dental Care 04 layout',
    'description': 'A clean and modern Odoo website theme designed for medical clinics or dental care centers.',
    'category': 'Website',
    'depends': ['website'],
    'data': [
        'views/templates.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'royal_clinic_theme/static/src/css/dental_style.css',
        ],
    },
    'license' : 'LGPL-3',
    'installable': True,
    'application': True,
}
