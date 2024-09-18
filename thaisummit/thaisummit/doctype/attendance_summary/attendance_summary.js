// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance Summary', {
	refresh:function(frm){
		frm.fields_dict.html.$wrapper.empty()
		frm.disable_save()
		frappe.model.clear_table(frm.doc,"attendance");
		if (!frappe.user.has_role('System Manager')) {
			frappe.db.get_value("Employee",{'user_id':frappe.session.user},['department'], (r) => {
				if (r){
					console.log(r.department)
					frm.set_query('employee', function(doc) {
						return {
							filters: {
								"status": "Active",
								"department" : r.department
							}
						};
					})
				}
			});
		}
		frappe.db.get_value("Employee",{'user_id':frappe.session.user},['employee','employee_name'], (r) => {
			if (r){
				frm.set_value('employee',r.employee)
				frm.set_value('employee_name',r.employee_name)
			}
		})
		frm.set_value('to_date',frappe.datetime.add_days(frappe.datetime.month_start(), 24))
		var d = frappe.datetime.add_months(frappe.datetime.month_start(), -1)
		frm.set_value('from_date',frappe.datetime.add_days(d, 25))
	},
	onload(frm){
		frm.disable_save()
		console.log(frappe.session.user)
		console.log("HI")
		if (!frappe.user.has_role('System Manager')) {
			frappe.db.get_value("Employee",{'user_id':frappe.session.user},['department'], (r) => {
				if (r){
					console.log(r.department)
					frm.set_query('employee', function(doc) {
						return {
							filters: {
								"status": "Active",
								"department" : r.department
							}
						};
					})
				}
			});
		}
		frm.fields_dict.html.$wrapper.empty()
		frappe.model.clear_table(frm.doc,"attendance");
		frappe.call({
			method:'thaisummit.thaisummit.doctype.attendance_summary.attendance_summary.get_employee',
			args:{
			},
			callback(r){
				frm.set_value('employee',r.message[0])
				frm.set_value('employee_name',r.message[1])
			}
		})
	},
	employee(frm){
		frm.trigger('get_data')
	},
	from_date(frm){
		frm.trigger('get_data')
	},
	to_date(frm){
		frm.trigger('get_data')
	},
	get_data: function (frm) {
		if (frm.doc.from_date && frm.doc.to_date && frm.doc.employee) {
			if (!frappe.is_mobile()) {
				frm.trigger('get_data_system')
			}
			else {
				frm.trigger('get_data_mobile')
			}
		}
	},
	get_data_system(frm) {
		if (frm.doc.employee) {
			frappe.call({
				method: "thaisummit.thaisummit.doctype.attendance_summary.attendance_summary.get_data_system",
				args: {
					emp: frm.doc.employee,
					from_date: frm.doc.from_date,
					to_date: frm.doc.to_date
				},
				callback: function (r) {
					frm.fields_dict.html.$wrapper.empty().append(r.message)
				}
			})
		}
		else {
			frm.fields_dict.html.$wrapper.empty().append("<center><h2>Attendance Not Found</h2></center>")
		}
	},
	get_data_mobile(frm) {
		if (frm.doc.employee) {
			frappe.call({
				method: "thaisummit.thaisummit.doctype.attendance_summary.attendance_summary.get_data_system",
				args: {
					emp: frm.doc.employee,
					from_date: frm.doc.from_date,
					to_date: frm.doc.to_date
				},
				callback: function (r) {
					frm.fields_dict.html.$wrapper.empty().append(r.message)
				}
			})
		}
		else {
			frm.fields_dict.html.$wrapper.empty().append("<center><h2>Attendance Not Found</h2></center>")
		}
	},
});
