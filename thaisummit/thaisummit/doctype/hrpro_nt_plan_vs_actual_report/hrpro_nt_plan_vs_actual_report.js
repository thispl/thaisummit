// Copyright (c) 2023, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('HRPRO NT Plan vs Actual Report', {
	refresh: function (frm) {
		// frm.disable_save()
		if (frm.doc.date) {
			if (frm.doc.shift != 'Full Day') {
				frm.call('shiftwise_report').then(r => {
					if (r.message) {
						frm.fields_dict.report.$wrapper.empty().append(r.message)
					}
				})
			}
			else{
				frm.call('withoutshift_report').then(r => {
					if (r.message) {
						frm.fields_dict.report.$wrapper.empty().append(r.message)
					}
				})
			}
		}
	},
});
