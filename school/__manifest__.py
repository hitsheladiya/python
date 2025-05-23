{
	'name' : 'School Managment',
	'version' : '1.1',
	'summary' : 'School Managment System',
	'sequence' : 1,
	'description' : 'My School Managment System Software Supported In Odoo v18',
	'category' : 'School',
	'website' : 'htpps://school.system.com',
	'depends' : ['base'],
	"data": [
		"security/ir.model.access.csv",
		"views/school_view_action.xml",
		"views/course_view_action.xml",
		"views/class_view_action.xml",
		"views/student_view_action.xml",
		"views/teacher_view_action.xml",
		"views/menu_items.xml",
	],
	'demo' : [],
	'application' : False,
	'installable' : True,
	'auto_install' : False,
	'license' : 'LGPL-3',
}