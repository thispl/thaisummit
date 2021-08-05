// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('CL Plan vs Actual', {
	refresh: function(frm) {
		if (frm.doc.date) {
				frm.call('get_data').then(r => {
					if (r.message) {
						frm.fields_dict.html.$wrapper.empty().append(r.message)
					}
				})
	
		}
	}
});
