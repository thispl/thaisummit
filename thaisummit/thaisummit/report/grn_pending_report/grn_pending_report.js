// Copyright (c) 2016, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["GRN Pending Report"] = {
	"filters": [
		{
			"fieldname": "mat_no",
			"label": __("Mat No"),
			"fieldtype": "Link",
			"options": "TSAI Part Master",
			"reqd": 1,
		}
	]
};
