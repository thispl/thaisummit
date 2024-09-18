// Copyright (c) 2023, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('RM Input', {
	// refresh: function(frm) {

	// }
	save_iym_old_data: function (frm) {
		frm.call('get_old_iym').then(r => {
			console.log('hi')
		})
	},
	save_re_old_data: function (frm) {
		frm.call('get_old_re').then(r => {
			console.log('hi')
		})
	}
});
