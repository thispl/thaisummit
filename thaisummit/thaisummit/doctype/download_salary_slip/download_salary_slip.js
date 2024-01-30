// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Download Salary Slip', {
	refresh: function (frm) {
		if (!frappe.user.has_role('System Manager')) {
			frappe.db.get_value("Employee",{'user_id':frappe.session.user},['employee','employee_name'], (r) => {
				if (r){
					frm.set_value('employee',r.employee)
				}
			})
			frm.set_df_property("employee","read_only",1)
		}
		else{
			frm.set_df_property("employee","read_only",0)
		}
		frm.disable_save()
	},
	month(frm) {
		frm.trigger('get_slip')
	},
	year(frm) {
		frm.trigger('get_slip')
	},
	employee(frm) {
		frm.trigger('get_slip')
	},
	get_slip(frm) {
		if (frm.doc.employee && frm.doc.month && frm.doc.year) {
			frm.call('get_salary_slip')
				.then((r) => {
					if (r.message) {
						frm.set_value('salary_slip', r.message[0].name)
					}
					else {
						frm.set_value('salary_slip','')
						frappe.msgprint("Salary Slip Not Found")
					}
				})
		}
	},
	download(frm) {
		if (frm.doc.employee && frm.doc.month && frm.doc.year && frm.doc.salary_slip) {
			window.open(
				frappe.urllib.get_full_url(`/api/method/frappe.utils.print_format.download_pdf?
				doctype=${encodeURIComponent("Salary Slip")}
				&name=${encodeURIComponent(frm.doc.salary_slip)}
				&format=${encodeURIComponent('Salary Slip New')}`)
			);
		}
		else if(!frm.doc.employee){
			frappe.msgprint('Please choose Employee ID')
		}
		else if(!frm.doc.month){
			frappe.msgprint('Please choose Month')
		}else if(!frm.doc.year){
			frappe.msgprint('Please choose Year')
		}
		else if(!frm.doc.salary_slip){
			frappe.msgprint('Salary Slip Not Found')
		}
	}
});
