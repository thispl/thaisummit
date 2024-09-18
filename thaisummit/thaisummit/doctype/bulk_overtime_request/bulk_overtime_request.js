// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bulk Overtime Request', {
	refresh: function (frm) {
		frm.disable_save()
		frm.set_value("requested_by", frappe.session.user)
		if (frm.doc.employees) {
			frm.add_custom_button(__('Submit Overtime'), function () {
				frm.call('create_overtime_request')
			});
		}
	},

});
frappe.ui.form.on('Bulk OT', {
	employee(frm, cdt, cdn) {
		var child = locals[cdt][cdn]
		if (!frm.doc.approver) {
			frappe.db.get_value("Employee", { "name": child.employee }, "department", (r) => {
				if (r.department) {
					frappe.call({
						method: 'thaisummit.custom.get_approver',
						args: {
							department: r.department,
							employee: child.employee
						},
						callback(r) {
							if (r.message) {
								frm.set_value("approver", r.message)
								frappe.db.get_value("Employee", { "user_id": r.message }, ["name", "employee_name"], (r) => {
									frm.set_value("approver_id", r.name)
									frm.set_value("approver_name", r.employee_name)
								});
							}
						}
					})
				}
			});
		}
		$.each(frm.doc.employees, function (i, d) {
			if (child.idx > 1) {
				if (d.idx == (child.idx - 1)) {
					child.ot_date = d.ot_date
					child.from_time = d.from_time
					child.to_time = d.to_time
					child.total_hours = d.total_hours
					child.ot_hours = d.ot_hours
					child.shift = d.shift
				}
				frm.refresh_field('employees')
			}
		})
	},
	shift(frm, cdt, cdn) {
		var child = locals[cdt][cdn]
		if (child.ot_date) {
			if (child.shift) {
				if (child.shift == '1') {
					frm.call('check_holiday', {
						ot_date: child.ot_date
					}).then(r => {
						if (r.message == 'NO') {
							frappe.msgprint("Overtime Request for Shift 1 can be applied only on Sunday or Holiday")
							child.from_time = ''
							frm.refresh_field('employees')
						}
						else {
							frappe.db.get_value('Shift Type', child.shift, 'start_time', (r) => {
								child.from_time = r.start_time
								child.to_time = ''
								child.ot_hours = ''
								child.total_hours = ''
								frm.refresh_field('employees')
							})
						}
					})
				}
				else {
					frappe.db.get_value('Shift Type', child.shift, 'start_time', (r) => {
						child.from_time = r.start_time
						child.to_time = ''
						child.ot_hours = ''
						child.total_hours = ''
						frm.refresh_field('employees')
					})
				}

			}

		}
		else {
			frappe.throw("Please enter Shift")
		}
	},
	from_time(frm, cdt, cdn) {
		var child = locals[cdt][cdn]
		if (child.to_time) {
			frappe.call({
				"method": "thaisummit.thaisummit.doctype.overtime_request.overtime_request.ot_hours",
				args: {
					'ot_date': child.ot_date,
					'shift': child.shift,
					"from_time": child.from_time,
					"to_time": child.to_time
				},
				callback(r) {
					child.ot_hours = r.message[1]
					child.total_hours = r.message[0]
					frm.refresh_field('employees')
				}
			})
		}
		if (child.from_time) {
			frappe.call({
				method: 'thaisummit.custom.roundoff_time',
				args: {
					time: child.from_time
				},
				callback(r) {
					if (r.message) {
						child.from_time = r.message
						frm.refresh_field('employees')
					}
				}
			})
			// frm.call('get_shift', {
			// 	ot_date: child.ot_date,
			// 	from_time: child.from_time,
			// }).then(r => {
			// 	child.shift = r.message[0]
			// 	child.from_time = r.message[1]
			// 	if (r.message[1] == "") {
			// 		child.total_hours = ""
			// 		child.ot_hours = ""
			// 		child.shift = ""
			// 	}
			// 	frm.refresh_field('employees')
			// })
		}
	},
	to_time(frm, cdt, cdn) {
		frm.refresh_field('employees')
		var child = locals[cdt][cdn]
		if (child.from_time) {
			frappe.call({
				"method": "thaisummit.thaisummit.doctype.overtime_request.overtime_request.ot_hours",
				args: {
					'ot_date': child.ot_date,
					'shift': child.shift,
					"from_time": child.from_time,
					"to_time": child.to_time
				},
				callback(r) {
					child.ot_hours = r.message[1]
					child.total_hours = r.message[0]
					frm.refresh_field('employees')
				}
			})
			// frm.refresh_field('employees')
		}
		if(child.to_time){
			frappe.call({
				method: 'thaisummit.custom.roundoff_time',
				args: {
					time: child.to_time
				},
				callback(r) {
					if (r.message) {
						child.to_time = r.message
						frm.refresh_field('employees')
					}
				}
			})
		}
	},
	ot_date(frm, cdt, cdn) {
		var child = locals[cdt][cdn]
		if (!frappe.user.has_role('HR GM')) {
		if (child.ot_date){
			var date = frappe.datetime.add_days(child.ot_date,3 )
			frappe.call({
			    "method":"thaisummit.utils.get_server_date" ,
			    callback(r){
				    if (r.message > date) {
						frappe.msgprint("OT should be applied within 3 days")
						frappe.validated = false;
						child.ot_date = ''
						frm.refresh_field('employees')
					}
			    }
			})
		}
	}
		// if (child.ot_date) {
		// 	frappe.call({
		// 		method: 'thaisummit.custom.application_allowed_from',
		// 		args: {
		// 			date: child.ot_date
		// 		},
		// 		callback(r) {
		// 			if (r.message == 'NO') {
		// 				child.ot_date = ''
		// 				frm.refresh_field('employees')
		// 			}
		// 		}
		// 	})
		// }
	}
})