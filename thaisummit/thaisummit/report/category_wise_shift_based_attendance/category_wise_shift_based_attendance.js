// Copyright (c) 2016, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Category Wise Shift Based Attendance"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default":"2021-08-01"
			
			}
		,
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default":"2021-08-30"
			
		},
		
		{
			"fieldname": "employee_type",
			"label": __("Employee Type"),
			"fieldtype": "Select",
			"reqd": 1,
			"options": ["WC", "BC", "FT", "NT", "CL"],
			"default": "WC"
		}
	],
	
}