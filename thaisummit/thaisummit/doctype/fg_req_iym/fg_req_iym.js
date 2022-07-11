// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('FG REQ IYM', {
	refresh: function(frm) {
		frappe.breadcrumbs.add("Home","E-KANBAN");
		frm.disable_save()
		frm.call('get_data').then(r=>{
			if (r.message) {
				frm.fields_dict.iym.$wrapper.empty().append(r.message)
			}
		})
	},
});
