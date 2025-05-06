{
    'name': 'Retail Access Rights',
    'version': '1.0',
    'category': 'Security',
    'summary': 'Custom access rights for Cashiers, Inventory Staff, Store Managers, and Admins',
    'depends': ['sale', 'stock','product'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/access_rules.xml',
        'views/menu.xml',
    ],
    'license': "LGPL-3",
    'installable': True,
    'application': True,
}
