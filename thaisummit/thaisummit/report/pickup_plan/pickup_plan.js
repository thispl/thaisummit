// Copyright (c) 2016, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pickup Plan"] = {
	"filters": [
		{			
			"fieldname":"supplier_code",
			"label": __("Supplier Code"),
			"fieldtype": "Link",
			"options": "TSAI Supplier",
			"reqd": '1'
		},
	],
	refresh(frm){
        frappe.breadcrumbs.add("Home","E-KANBAN");
	}
};
