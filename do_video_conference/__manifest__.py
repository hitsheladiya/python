# -*- coding: utf-8 -*-
{
	'name': 'Video Conference With JITSI And BigBlueButtons',
	'summary': """
		This modules support Video Conference With JITSI And BigBlueButtons.
	""",
	'description': """
		This modules support for Video Conference With JITSI And BigBlueButtons.
	""",
	'author': 'Do Incredible',
	'website': 'http://doincredible.com',
	'license': 'OPL-1',
	'category': 'Calendar',
	'sequence': '10',
	'version': '1.0.0',
	'depends': ['website', 'calendar', 'attachment_indexation', 'website_livechat', 'project_todo','portal'],
	'data': [
		'security/ir.model.access.csv',
		'security/meeting_security.xml',
		'data/ir_config_data.xml',
		'data/calendar_mail_data.xml',
		'data/otp_mail_template.xml',
		'views/calendar_views.xml',
		'views/res_config_setting_views.xml',
		'views/website_attachment.xml',
		'views/calendar_templates.xml',
		'views/calender_portal_templates.xml',
	],
	'assets': {
		'web.assets_frontend': [
			'/do_video_conference/static/lib/select2/select2.css',
			'/do_video_conference/static/lib/select2/select2.min.js',
			'/do_video_conference/static/lib/jquery-confirm/dist/jquery-confirm.min.css',
			'/do_video_conference/static/lib/jquery-confirm/dist/jquery-confirm.min.js',
			'/do_video_conference/static/lib/ckeditor5/build/ckeditor.js',
			'/do_video_conference/static/lib/lightGallery/src/css/lightgallery.css',
			'/do_video_conference/static/lib/lightGallery/lib/jquery.mousewheel.min.js',
			'/do_video_conference/static/lib/lightGallery/src/js/lightgallery.js',
			'/do_video_conference/static/lib/lightGallery/modules/lg-fullscreen.min.js',
			'/do_video_conference/static/lib/lightGallery/modules/lg-zoom.js',
			'/do_video_conference/static/lib/gridstack/src/gridstack.scss',
			'/do_video_conference/static/lib/gridstack/src/gridstack.js',
			'/do_video_conference/static/lib/gridstack/src/gridstack.jQueryUI.js',
			'/do_video_conference/static/lib/DataTables/datatables.js',
			'/do_video_conference/static/lib/DataTables/datatables.css',
			'/do_video_conference/static/src/scss/website.scss',
			'/do_video_conference/static/src/js/video_conference.js',
			'/do_video_conference/static/src/js/metting_attachment.js',
			'/do_video_conference/static/src/scss/meeting_portal.scss',
			'/do_video_conference/static/src/js/meeting_portal.js'
		]
	},
	'application': True,
	'price': 350,
	'currency': 'USD',
	'installable': True,
	'application': True,
	'images': ['static/description/images/1.png'],
}
