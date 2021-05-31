// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Manual Attendance Correction Request', {
	refresh: function (frm) {
		frappe.breadcrumbs.add("HR");
		// if (frappe.user.has_role('Employee')) {
		frm.fields_dict['mp_child'].grid.wrapper.find('.grid-add-row').hide();
		frm.fields_dict['mp_child'].grid.wrapper.find('.btn-open-row').hide();
		frm.disable_save()
		frm.set_value("from_date", frappe.datetime.nowdate());
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
				if(r.message){
				frm.set_value("employee", r.message.employee)
				frm.set_value("employee_name", r.message.employee_name)
			}
		}
		})
	// }
	},
	mp_child_on_form_rendered:function(frm, cdt, cdn){
		frm.fields_dict['mp_child'].grid.wrapper.find('.grid-delete-row').hide();
		frm.fields_dict['mp_child'].grid.wrapper.find('.grid-duplicate-row').hide();
		frm.fields_dict['mp_child'].grid.wrapper.find('.grid-move-row').hide();
		frm.fields_dict['mp_child'].grid.wrapper.find('.grid-append-row').hide();
		frm.fields_dict['mp_child'].grid.wrapper.find('.grid-insert-row-below').hide();
		frm.fields_dict['mp_child'].grid.wrapper.find('.grid-insert-row').hide();
	},
	from_date: function (frm) {
		if(frm.doc.from_date){
		frm.trigger('get_att')
		}
	},
	employee: function (frm) {
		if(frm.doc.from_date){
		frm.trigger('get_att')
		}
	},
	get_att(frm){
		frm.clear_table('mp_child')
		frm.call('get_att')
			.then((att_list) => {
				console.log(att_list)
				$.each(att_list.message, function (i, d) {
					var c_list = [d.in_time,d.out_time,d.qr_scan_time]
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
							'qr_scan_time': d.qr_scan_time
						})

					}
				})
				frm.refresh_field('mp_child')
			})
	}
});

frappe.ui.form.on('MP Child', {
	submit(frm, cdt, cdn) {
		var child = locals[cdt][cdn]
		if (!child.in_time) {
			frappe.throw("Please Enter IN Time")
		}
		if (!child.out_time) {
			frappe.throw("Please Enter OUT Time")
		}
		if (!child.qr_scan_time) {
			frappe.throw("Please Enter QR Scan Time")
		}
		if (child.in_time && child.out_time && child.qr_scan_time) {
			frm.call('create_miss_punch_application', {
				row: child,
				from_date: frm.doc.from_date,
			}).then((mp) => {
				if (mp.message == 'ok') {
					frm.get_field("mp_child").grid.grid_rows[child.idx - 1].remove();
					frm.refresh_field('mp_child')
					frappe.msgprint('Success')
				}
			})
		}
	},
	in_time(frm, cdt, cdn) {
		var child = locals[cdt][cdn]
		if (child.in_time){
			child.correction = "IN Time"
			frm.refresh_field('mp_child')
		}
	},
	out_time(frm, cdt, cdn) {
		var child = locals[cdt][cdn]
		if (child.out_time){
			child.correction = "OUT Time"
			frm.refresh_field('mp_child')
		}
	},
	qr_scan_time(frm, cdt, cdn) {
		var child = locals[cdt][cdn]
		if (child.qr_scan_time){
			child.correction = "QR Scan Time"
			frm.refresh_field('mp_child')
		}
	}
})