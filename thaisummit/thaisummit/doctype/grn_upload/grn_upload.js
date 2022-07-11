// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('GRN Upload', {
	refresh: function(frm) {
		if (frm.doc.__islocal){
			frm.set_value('date',frappe.datetime.get_today())
		}
	}
});
