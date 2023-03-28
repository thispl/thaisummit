// Copyright (c) 2023, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Generate Tag Card', {
	onload: function(frm) {
		if(frm.doc.docstatus == 1){
			frm.call('get_data').then(r=>{
				if (r.message) {
					frm.fields_dict.html.$wrapper.empty().append(r.message)
				}
			})

		}

	},
	quantity(frm){
		frm.call('get_child_mat').then(r=>{
			
		})
		frm.call('get_data').then(r=>{
			if (r.message) {
				frm.fields_dict.html.$wrapper.empty().append(r.message)
			}
		})
		
	},
});
