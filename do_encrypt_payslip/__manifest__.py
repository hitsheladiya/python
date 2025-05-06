# -*- encoding: utf-8 -*-

{
    'name': 'Encrypt Payslip Report',
    'category': 'Payslip',
    'author': 'Do Incredible',
    'license': 'OPL-1',
    'sequence': '10',
    'summary': 'Encrypt Payslip Report',
    'website': 'https://doincredible.com',
    'version': '18.0.1.0.0',
    'description': "Encrypt Payslip Report",
    'depends': ['base','hr_payroll'],
    'data': [
        "views/hr_employee_view.xml",
    ],
    'installable': True,
    'application': True,
    'images': [],
}