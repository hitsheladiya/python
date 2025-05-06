# -*- encoding: utf-8 -*-

{
	'name': 'Global Search',
	'category': 'Search',
	'author': 'Do Incredible',
	'license': 'OPL-1',
	'sequence': '10',
	'summary': 'Global Search',
	'website': 'https://doincredible.com',
	'version': '1.0',
	'description': "Global Search",
	'depends': ['base','web'],
	'data': [
		'security/ir.model.access.csv',
		'wizard/global_search_wizard_view.xml',
	],
	"assets": {
		"web.assets_backend": [
			"do_global_search/static/src/js/wizard.js",
			"do_global_search/static/src/js/global_icon.js",
			"do_global_search/static/src/xml/global_icon.xml",
		],
	},
	'installable': True,
	'application': True,
	'images': [],
}