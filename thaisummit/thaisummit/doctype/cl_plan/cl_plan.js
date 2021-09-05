// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('CL Plan', {
	// refresh: function(frm) {

	// },
	validate(frm){
		// if(frm.doc.upload){
		// 	frappe.call({
		// 		method: "thaisummit.thaisummit.doctype.cl_plan.cl_plan.upload",
		// 		args:{
		// 			file : frm.doc.upload
		// 		}
		// 	})
		// }
	},
	upload(frm){
		if(frm.doc.upload){
			frappe.call({
				method: "thaisummit.thaisummit.doctype.cl_plan.cl_plan.validate_csv",
				args:{
					file : frm.doc.upload,
					from_date : frm.doc.from_date,
					to_date : frm.doc.to_date
				},
			})
		}
	},
	after_save(frm){
		if(frm.doc.upload){
			frappe.call({
				method: "thaisummit.thaisummit.doctype.cl_plan.cl_plan.create_cl_head_count_plan",
				args:{
					file : frm.doc.upload
				},
				freeze: true,
				freeze_message: 'Submitting CL Plan....',
			})
		}
	},
	get_template: function (frm) {
		window.location.href = repl(frappe.request.url +
			'?cmd=%(cmd)s&from_date=%(from_date)s&to_date=%(to_date)s', {
			cmd: "thaisummit.thaisummit.doctype.cl_plan.cl_plan.get_template",
			from_date: frm.doc.from_date,
			to_date: frm.doc.to_date,
		});
	},
	to_date(frm){
		if(frm.doc.from_date && frm.doc.to_date){
		if (frm.doc.to_date < frm.doc.from_date) {
				frappe.msgprint("To Date should not be greater than From Date")
				frm.set_value('to_date', '')
			}
		}
	}
});
