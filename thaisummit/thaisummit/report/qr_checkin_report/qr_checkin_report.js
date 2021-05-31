// Copyright (c) 2016, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["QR Checkin Report"] = {
	"filters": [
		{
			"fieldname": "date",
			"label": __("Date"),
			"fieldtype": "Date",
			"reqd": 1 ,
			"default": frappe.datetime.nowdate()
		},
		{
			"fieldname": "shift_type",
			"label": __("Shift Type"),
			"fieldtype": "Link",
			"reqd": 1 ,
			"options": "Shift Type",
			"default": "1"
		},
	],
	onload: function(report) {
		console.log(report)
	}
};


