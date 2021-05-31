// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Overtime Request', {
	refresh: function(frm) {
		frappe.breadcrumbs.add("HR","Overtime Request");
	},
	employee(frm) {
		if (frm.doc.employee) {
			if (frm.doc.approver) {
				frappe.call({
					"method": "frappe.client.get",
					args: {
						doctype: "Employee",
						filters: { "user_id": frm.doc.approver },
						fieldname: ["name", "employee_name"]
					},
					callback(r) {
						console.log(r.message)
						if (r.message.name) {
							frm.set_value('approver_id', r.message.name)
							frm.set_value('approver_name', r.message.employee_name)
						}
						else {
							console.log('hi')
							frm.set_value('approver_id', '')
							frm.set_value('approver_name', '')
						}
					}
				})
			} else {
				frm.set_value('approver_id', '')
				frm.set_value('approver_name', '')
			}
		}
	},
	to_time(frm) {
		if (frm.doc.from_time) {
			frappe.call({
				"method": "thaisummit.thaisummit.doctype.overtime_request.overtime_request.ot_hours",
				args: {
					'from_time': frm.doc.from_time,
					"to_time": frm.doc.to_time
				},
				callback(r) {
					frm.set_value('ot_hours', r.message)
				}
			})
		}
	},
	from_time(frm) {
		if (frm.doc.to_time) {
			frm.trigger('to_time')
		}
	}
});
