// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('TSA Master', {
	// refresh: function(frm) {

	// }
	iym_model_code(frm){
		frappe.call({
			method:"thaisummit.thaisummit.doctype.tsa_master.tsa_master",
			args:{
				d:frm.doc.iym_model_code,	
			},
		})
	}
});
