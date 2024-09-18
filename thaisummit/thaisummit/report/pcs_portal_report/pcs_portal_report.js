// Copyright (c) 2016, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PCS Portal Report"] = {
	"filters": [
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Select",
			"reqd": 1,
			"default": 'IYM',
			"options": ['IYM','RE']
		},
	]
};
