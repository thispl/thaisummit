frappe.ui.form.on('Manual Attendance Correction Approval', {
	refresh: function (frm) {
		frappe.breadcrumbs.add("HR");
		if (frappe.user.has_role(['HOD', 'HR GM'])) {
			frm.fields_dict['mp_child_approval'].grid.wrapper.find('.grid-add-row').hide();
			frm.fields_dict['mp_child_approval'].grid.wrapper.find('.btn-open-row').hide();
			frm.disable_save()
			frm.set_value("from_date", frappe.datetime.month_start());
			frm.set_value("to_date", frappe.datetime.month_end());
		}
		frm.trigger("highlight_changes")
	},


	mp_child_approval_on_form_rendered: function (frm, cdt, cdn) {
		frm.fields_dict['mp_child_approval'].grid.wrapper.find('.grid-delete-row').hide();
		frm.fields_dict['mp_child_approval'].grid.wrapper.find('.grid-duplicate-row').hide();
		frm.fields_dict['mp_child_approval'].grid.wrapper.find('.grid-move-row').hide();
		frm.fields_dict['mp_child_approval'].grid.wrapper.find('.grid-append-row').hide();
		frm.fields_dict['mp_child_approval'].grid.wrapper.find('.grid-insert-row-below').hide();
		frm.fields_dict['mp_child_approval'].grid.wrapper.find('.grid-insert-row').hide();
	},
	from_date: function (frm) {

		if (frm.doc.from_date && frm.doc.to_date) {
			if (frappe.user.has_role('HOD')) {
				frm.trigger('get_mp_hod')
			}
			else if (frappe.user.has_role('HR GM')) {
				frm.trigger('get_mp_hr')
			}
		}
		
		$.each(frm.doc.mp_child_approval, function (i, d) {
			
		})
		frm.trigger("highlight_changes")

	},
	to_date: function (frm) {
		if (frm.doc.from_date && frm.doc.to_date) {
			if (frappe.user.has_role('HOD')) {
				frm.trigger('get_mp_hod')
			}
			else if (frappe.user.has_role('HR GM')) {
				frm.trigger('get_mp_hr')
			}
		}
	},

	highlight_changes(frm) {
		$.each(frm.doc.mp_child_approval, function (i, d) {
			if(d.correction == 'IN Time'){
				$("div[data-fieldname='in_time']")[i+1].setAttribute("style", "background-color:yellow;");
			}

			if(d.correction == 'OUT Time'){
				$("div[data-fieldname='out_time']")[i+1].setAttribute("style", "background-color:yellow;");
			}
			if(d.correction == 'QR Scan Time'){
				$("div[data-fieldname='qr_scan_time']")[i+1].setAttribute("style", "background-color:yellow;");
			}
		})
	},
	get_mp_hod(frm) {
		frm.clear_table('mp_child_approval')
		frm.call('get_mp_hod')
			.then((mp_list) => {
				$.each(mp_list.message, function (i, d) {
					frm.add_child('mp_child_approval', {
						'employee': d.employee,
						'employee_name': d.employee_name,
						'attendance': d.attendance,
						'shift': d.shift,
						'attendance_date': d.attendance_date,
						'miss_punch_application': d.name,
						'in_time': d.in_time,
						'out_time': d.out_time,
						'qr_scan_time': d.qr_scan_time,
						'correction': d.correction
					})
				})
				frm.refresh_field('mp_child_approval')
				frm.trigger("highlight_changes")
			})
	},
	get_mp_hr(frm) {
		frm.clear_table('mp_child_approval')
		frm.call('get_mp_hr')
			.then((mp_list) => {
				$.each(mp_list.message, function (i, d) {
					frm.add_child('mp_child_approval', {
						'employee': d.employee,
						'employee_name': d.employee_name,
						'attendance': d.name,
						'shift': d.shift,
						'attendance_date': d.attendance_date,
						'miss_punch_application': d.name,
						'in_time': d.in_time,
						'out_time': d.out_time,
						'qr_scan_time': d.qr_scan_time,
						'correction': d.correction
					})
				})
				frm.refresh_field('mp_child_approval')
			})
	}
});


// })

frappe.ui.form.on("MP Child Approval", "onload", function (frm, cdt, cdn) {
	console.log('hi')
	var child = locals[cdt][cdn];
	cur_frm.doc.mp_child_approval.forEach(function (child) {
		var sel = format('div[data-fieldname="mp_child_approval"] > div.grid-row[data-idx="{0}"]', [child.idx]);
		if (child.amount > 1000) {
			$(sel).css('background-color', "#ff5858");
		} else {
			$(sel).css('background-color', 'red');
		}
	});
});

// frappe.ui.form.on('MP Child Approval', {
// 	approve(frm, cdt, cdn) {
// 		var child = locals[cdt][cdn]
// 		if (!child.in_time) {
// 			frappe.throw("Please Enter IN Time")
// 		}
// 		if (!child.out_time) {
// 			frappe.throw("Please Enter OUT Time")
// 		}
// 		if (!child.qr_scan_time) {
// 			frappe.throw("Please Enter QR Scan Time")
// 		}
// 		if (frappe.user.has_role('HOD')) {
// 			if (child.in_time && child.out_time && child.qr_scan_time) {
// 				frm.call('approve_miss_punch_hod', {
// 					row: child,
// 					from_date: frm.doc.from_date,
// 					to_date: frm.doc.to_date
// 				}).then((mp) => {
// 					if (mp.message == 'ok') {
// 						frm.get_field("mp_child_approval").grid.grid_rows[child.idx - 1].remove();
// 						frm.refresh_field('mp_child_approval')
// 						frappe.msgprint('Approved')
// 					}
// 				})
// 			}
// 		}
// 		if (frappe.user.has_role('HR GM')) {
// 			if (child.in_time && child.out_time && child.qr_scan_time) {
// 				frm.call('approve_miss_punch_hr', {
// 					row: child,
// 					from_date: frm.doc.from_date,
// 					to_date: frm.doc.to_date
// 				}).then((mp) => {
// 					if (mp.message == 'ok') {
// 						frm.get_field("mp_child_approval").grid.grid_rows[child.idx - 1].remove();
// 						frm.refresh_field('mp_child_approval')
// 						frappe.msgprint('Approved')
// 					}
// 				})
// 			}
// 		}
// 	},
// })