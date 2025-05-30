{
	'name' : 'Hospital Managment',
	'version' : '1.1',
	'summary' : 'Hospital Managment System',
	'sequence' : 1,
	'description' : 'My Hospital Managment System Software Supported In Odoo v18',
	'category' : 'Hospital',
	'website' : 'htpps://hospital.system.com',
	'depends' : ['base','mail'],
	"data": [
		"security/ir.model.access.csv",
		"wizard/hospital_wizard_view.xml",
		"views/hospital_view_action.xml",
		"views/patient_view_action.xml",
		"views/doctor_view_action.xml",
		"views/medicinename_view_action.xml",
		"views/appointment_view_action.xml",
		"views/menu_items.xml",
	],
	'demo' : [],
	'application' : False,
	'installable' : True,
	'auto_install' : False,
	'license' : 'LGPL-3',
}