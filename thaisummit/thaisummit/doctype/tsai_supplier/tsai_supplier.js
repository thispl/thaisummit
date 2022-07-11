// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('TSAI Supplier', {
	refresh: function(frm) {
		
	},
	invoice_no_type(frm){
		if (frm.doc.__islocal){
			if (frm.doc.invoice_no_type == 'Automatic'){
			var prefix = frm.doc.supplier_code + '-' + 'YYYY'
			frm.set_value('prefixed_running_no',prefix)
			var cur_no = frm.doc.supplier_code + '-' + 'YYYY' + '-000001'
			frm.set_value('current_running_no',cur_no)
			}
		}
	}
});
