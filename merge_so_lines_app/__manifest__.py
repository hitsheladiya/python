{
	'name' : 'Marge Sales',
	'version' : '18.0',
	'summary' : 'Marge Sales Order',
	'category' : 'Sales',
	'depends' : ['base','sale'],
	"data": [
		"views/marge_line.xml",
		"wizard/sale_marge_wizard.xml",
		"security/ir.model.access.csv",
	],
	'application' : False,
	'installable' : True,
	'auto_install' : False,
	'license' : 'LGPL-3',
}