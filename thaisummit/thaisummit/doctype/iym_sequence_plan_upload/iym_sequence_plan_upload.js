// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('IYM Sequence Plan Upload', {
	refresh: function(frm) {
		if(frm.doc.__islocal){
			frm.set_value('upload_date',frappe.datetime.nowdate())
		}
	},
	// attach(frm){
	// 	if(frm.doc.attach){
	// 		frm.call('read_xlsx',{
	// 		})
	// 	}
	// }
});
