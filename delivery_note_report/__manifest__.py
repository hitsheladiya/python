{
    'name': 'Natuber Delivery Note',
    'version': '1.0',
    'summary': 'Custom delivery note report for Natuber',
    'category': 'Sales',
    'depends': ['sale', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/delivery_note_view.xml',
        'views/menu.xml',
        'reports/delivery_note_template.xml',
    ],
    'license':'LGPL-3',
    'installable': True,
    'application': False,
}