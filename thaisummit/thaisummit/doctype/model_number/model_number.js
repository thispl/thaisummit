// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Model Number', {
	// refresh: function(frm) {

	// }
	model_number(frm){
		frm.set_value("model_barcode",frm.doc.model_number)
	},
	validate(frm){
		frm.set_value("model_barcode",frm.doc.model_number)
	}
});
