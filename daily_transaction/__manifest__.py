{
    'name': 'Daily Transaction Report',
    'version': '18.0',
    'summary': 'Generate PDF Daily Transaction Report',
    'depends': ['base','sale','account','web'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/daily_transaction_wizard_view.xml',
        'views/daily_transaction_report_menu.xml',
        'report/daily_transaction_report.xml',
        'report/daily_transaction_report_template.xml',
    ],
    'license' : 'LGPL-3',
    'installable': True,
    'application': True,
}