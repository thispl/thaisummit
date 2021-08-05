// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Manual Attendance Correction Request', {
	refresh: function (frm) {
		frappe.breadcrumbs.add("HR");
		// if (frappe.user.has_role('Employee')) {
		$('*[data-fieldname="mp_child"]').find('.grid-remove-rows').hide();
		$('*[data-fieldname="mp_child"]').find('.grid-remove-all-rows').hide();
		$('*[data-fieldname="mp_child"]').find('.grid-add-row').remove()
		frm.disable_save()
		// frm.set_value("from_date", frappe.datetime.nowdate());
		frappe.call({
			"method": "frappe.client.get_value",
			"args": {
				"doctype": "Employee",
				"filters": {
					"user_id": frappe.session.user
				},
				"fieldname": ["employee", "employee_name"]
			},
			callback(r) {
				if (r.message) {
					frm.set_value("employee", r.message.employee)
					frm.set_value("employee_name", r.message.employee_name)
				}
			}
		})
		// }
	},
	mp_child_on_form_rendered: function (frm, cdt, cdn) {
		frm.fields_dict['mp_child'].grid.wrapper.find('.grid-delete-row').hide();
		frm.fields_dict['mp_child'].grid.wrapper.find('.grid-duplicate-row').hide();
		frm.fields_dict['mp_child'].grid.wrapper.find('.grid-move-row').hide();
		frm.fields_dict['mp_child'].grid.wrapper.find('.grid-append-row').hide();
		frm.fields_dict['mp_child'].grid.wrapper.find('.grid-insert-row-below').hide();
		frm.fields_dict['mp_child'].grid.wrapper.find('.grid-insert-row').hide();
	},
	from_date: function (frm) {
		if (frm.doc.from_date) {
			frm.trigger('get_att')
		}
	},
	employee: function (frm) {
		if (frm.doc.from_date) {
			frm.trigger('get_att')
		}
	},
	get_att(frm) {
		frm.clear_table('mp_child')
		frm.call('get_att')
			.then((att_list) => {
				$.each(att_list.message, function (i, d) {
					var c_list = [d.in_time, d.out_time, d.qr_shift]
					if (c_list.includes(null)) {
						frm.add_child('mp_child', {
							'employee': d.employee,
							'employee_name': d.employee_name,
							'attendance': d.name,
							'department': d.department,
							'shift': d.shift,
							'attendance_date': d.attendance_date,
							'in_time': d.in_time,
							'out_time': d.out_time,
							'qr_shift': d.qr_shift
						})
					}
				})
				frm.refresh_field('mp_child')
			})
	},
	submit(frm) {
		$.each(frm.doc.mp_child, function (i, d) {
			if (!d.in_time) {
				frappe.throw("Please Enter IN Time")
			}
			if (!d.out_time) {
				frappe.throw("Please Enter OUT Time")
			}
			if (!d.qr_shift) {
				frappe.throw("Please Enter QR Scan Time")
			}
			if (d.in_time && d.out_time && d.qr_shift) {
				// frm.call('create_miss_punch_application', {
				// 	row: frm.doc.mp_child[0],
				// 	from_date: frm.doc.from_date,
				// }).then((mp) => {
				// 	if (mp.message == 'ok') {
				// 		frm.clear_table('mp_child')
				// 		// frm.get_field("mp_child").grid.grid_rows[child.idx - 1].remove();
				// 		// frm.refresh_field('mp_child')
				// 		frappe.msgprint('Manual Attendance Correction Submitted Successfully')
				// 		frm.reload_doc()
				// 	}
				// })
				frappe.call({
					method:'thaisummit.thaisummit.doctype.manual_attendance_correction_request.manual_attendance_correction_request.create_miss_punch',
					args:{
						row: frm.doc.mp_child[0],
						from_date: frm.doc.from_date,
					},
					callback(mp){
						if (mp.message == 'ok') {
							frm.clear_table('mp_child')
							frappe.msgprint('Manual Attendance Correction Submitted Successfully')
							frm.reload_doc()
						}
					}
				})
			}
		})
	},
});

// frappe.ui.form.on('MP Child', {

	// in_time(frm, cdt, cdn) {
	// 	var child = locals[cdt][cdn]
	// 	if (child.in_time){
	// 		child.correction = "IN Time"
	// 		frm.refresh_field('mp_child')
	// 	}
	// },
	// out_time(frm, cdt, cdn) {
	// 	var child = locals[cdt][cdn]
	// 	if (child.out_time){
	// 		child.correction = "OUT Time"
	// 		frm.refresh_field('mp_child')
	// 	}
	// },
	// qr_shift(frm, cdt, cdn) {
	// 	var child = locals[cdt][cdn]
	// 	if (child.qr_shift){
	// 		child.correction = "QR Scan Time"
	// 		frm.refresh_field('mp_child')
	// 	}
	// }
// })