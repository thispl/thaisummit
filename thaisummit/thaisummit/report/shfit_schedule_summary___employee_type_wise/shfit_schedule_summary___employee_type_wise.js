// Copyright (c) 2016, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Shfit Schedule Summary - Employee Type Wise"] = {
	"filters": [
		{
			"fieldname":"date",
			"label": __("Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.nowdate()
		},
	]
};
