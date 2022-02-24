// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Welfare Scan', {
	// refresh: function(frm) {

	// },
	scan(frm){
		if(frm.doc.welfare_occasion && frm.doc.welfare_item){
            location.href = "/welfare_scan";
		}
	}
});
