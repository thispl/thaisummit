// Copyright (c) 2023, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Download Bulk Salary Slip', {
	refresh: function(frm) {
		frm.disable_save();
	},
	download_slip(frm){
		if(frm.doc.start_date && frm.doc.employee_type){
			frappe.call({
				method:"thaisummit.thaisummit.doctype.download_bulk_salary_slip.salary_print.enqueue_download_multi_pdf",
				args:{
					doctype:"Salary Slip",
					employee_type: frm.doc.employee_type,
					start_date: frm.doc.start_date,
				},
				callback(r){
					if(r){
						console.log(r)
					}
				}
			})	
		}
	}
});
