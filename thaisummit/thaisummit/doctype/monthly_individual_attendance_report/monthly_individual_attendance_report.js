// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Monthly Individual Attendance report', {
	refresh(frm){
		frappe.breadcrumbs.add("Home")
		frm.disable_save()
		frappe.call({
			"method": "frappe.client.get_value",
			args: {
				doctype: "Employee",
				filters: { "user_id": frappe.session.user },
				fieldname: ["name", "employee_name"]
			},
			callback: function (r) {
				frm.set_value("employee",r.message.name)
				frm.set_value("employee_name",r.message.employee_name)
			}})
	},
	download: function (frm) {
		if (frm.doc.employee) {
			if (frm.doc.from_date && frm.doc.to_date ){
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: "thaisummit.thaisummit.doctype.monthly_individual_attendance_report.monthly_individual_attendance_report.download",
				args: 'employee=%(employee)s&from_date=%(from_date)s&to_date=%(to_date)s',
				from_date : frm.doc.from_date,
				to_date : frm.doc.to_date,
				employee : frm.doc.employee
			});
		}else{
			frappe.throw('Please Enter From Date and To Date')
		}
		}
		else{
			frappe.throw('Please Choose Employee')
		}
	},
});
