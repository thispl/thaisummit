// Copyright (c) 2016, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Order"] = {
	// "filters": [
	// 	{
	// 		'fieldname':'from_date',
	// 		'label':__('From_Date'),
	// 		'fieldtype':'Date',
	// 		'reqd':0
	// 	},
	// 	{
	// 		"fieldname": "to_date",
	// 		"label": __("To Date"),
	// 		"fieldtype": "Date",
	// 		"reqd": 0,
	// 		// "read_only": 0
	// 	},
	// ]
	refresh(frm){
        frappe.breadcrumbs.add("Home","E-KANBAN");
	}
};
