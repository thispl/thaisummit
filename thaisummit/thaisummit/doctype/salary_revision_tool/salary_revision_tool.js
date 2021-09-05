// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Salary Revision Tool', {
	refresh: function (frm) {
		if (frm.is_new()) {
			frm.set_value('date', frappe.datetime.now_date())
		}
	},
	get_template: function (frm) {
		console.log(frappe.request.url)
		window.location.href = repl(frappe.request.url +
			'?cmd=%(cmd)s&date=%(date)s&employee_type=%(employee_type)s', {
			cmd: "thaisummit.thaisummit.doctype.salary_revision_tool.salary_revision_tool.get_template",
			date: frm.doc.date,
			employee_type: frm.doc.employee_type,
		});
	},
	file(frm){
		frm.call('validate_file').then(r=>{
			if(r.message){
				frappe.throw(r.message)
			}
		})
	},
	validate(frm){
		frm.call('validate_file').then(r=>{
			if(r.message){
				frappe.throw(r.message)
			}
		})
	}
});
