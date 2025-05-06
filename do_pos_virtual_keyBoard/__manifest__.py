# -*- encoding: utf-8 -*-
{
	'name': 'POS Virtual KeyBoard',
	'category': 'POS',
	'author': 'Do Incredible',
	'license': 'OPL-1',
	'sequence': '10',
	'summary': 'Use a virtual keyboard for touchscreens',
	'website': 'https://doincredible.com',
	'version': '1.0',
	'description': """
	Use a virtual keyboard for touchscreens
	""",
	'depends': [
		'point_of_sale','web'
	],
	'data': [
		'views/pos_config_views.xml',
	],
	'assets': {
		'point_of_sale._assets_pos': [
			'do_pos_virtual_keyBoard/static/src/css/keyboard.css',
			'do_pos_virtual_keyBoard/static/src/app/screens/productscreen/onscreenkeyboard.js',
			'do_pos_virtual_keyBoard/static/src/app/screens/productscreen/input.js',
			'do_pos_virtual_keyBoard/static/src/app/screens/clientscreen/partner_list_screen.js',
			# 'do_pos_virtual_keyBoard/static/src/app/screens/clientscreen/partner_editor.js',
			'do_pos_virtual_keyBoard/static/src/app/popups/textarea_popup.js',
			'do_pos_virtual_keyBoard/static/src/app/popups/closing_popup.js',
			'do_pos_virtual_keyBoard/static/src/app/popups/cash_opening_popup.js',
			'do_pos_virtual_keyBoard/static/src/app/misc/search_bar.js',
			'do_pos_virtual_keyBoard/static/src/app/popups/cash_move_popup.js',
			'do_pos_virtual_keyBoard/static/src/xml/**/*',
		],
	},
	'installable': True,
	'application': True,
	'price': 50,
	'currency': 'USD',
	'images': ['static/description/images/1.png'],
	'live_test_url': '',
}