// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Approval', {
	refresh: function (frm) {
		frm.disable_save()
		$('*[data-fieldname="od_approval"]').find('.grid-remove-rows').hide();
		$('*[data-fieldname="od_approval"]').find('.grid-remove-all-rows').hide();
		$('*[data-fieldname="od_approval"]').find('.grid-add-row').remove()

		$('*[data-fieldname="pr_approval"]').find('.grid-remove-rows').hide();
		$('*[data-fieldname="pr_approval"]').find('.grid-remove-all-rows').hide();
		$('*[data-fieldname="pr_approval"]').find('.grid-add-row').remove()

		$('*[data-fieldname="la_approval"]').find('.grid-remove-rows').hide();
		$('*[data-fieldname="la_approval"]').find('.grid-remove-all-rows').hide();
		$('*[data-fieldname="la_approval"]').find('.grid-add-row').remove()

		$('*[data-fieldname="ot_approval"]').find('.grid-remove-rows').hide();
		$('*[data-fieldname="ot_approval"]').find('.grid-remove-all-rows').hide();
		$('*[data-fieldname="ot_approval"]').find('.grid-add-row').remove()

		$('*[data-fieldname="mp_approval"]').find('.grid-remove-rows').hide();
		$('*[data-fieldname="mp_approval"]').find('.grid-remove-all-rows').hide();
		$('*[data-fieldname="mp_approval"]').find('.grid-add-row').remove()

		$('*[data-fieldname="guest_entry_approval"]').find('.grid-remove-rows').hide();
		$('*[data-fieldname="guest_entry_approval"]').find('.grid-remove-all-rows').hide();
		$('*[data-fieldname="guest_entry_approval"]').find('.grid-add-row').remove()


		if (frappe.user.has_role(['HOD', 'GM', 'HR GM', 'CEO'])) {
			/* OD button start*/

			frm.fields_dict["od_approval"].grid.add_custom_button(__('Reject'),
				function () {
					$.each(frm.doc.od_approval, function (i, d) {
						if (d.__checked == 1) {
							// frappe.db.set_value('On Duty Application', d.on_duty_application, 'workflow_state', 'Rejected')
							frm.call('submit_doc', {
								doctype: "On Duty Application",
								name: d.on_duty_application,
								workflow_state: 'Rejected'
							})
							frm.get_field("od_approval").grid.grid_rows[d.idx - 1].remove();
						}
					})
				}).addClass('btn-danger')

			frm.fields_dict["od_approval"].grid.add_custom_button(__('Approve'),
				function () {
					$.each(frm.doc.od_approval, function (i, d) {
						if (d.__checked == 1) {
							if (d.vehicle_request == 0) {
								if (d.workflow_state == 'Pending for HOD') {
									// frappe.db.set_value('On Duty Application', d.on_duty_application, 'workflow_state', 'Pending for HR')
									// frm.get_field("od_approval").grid.grid_rows[d.idx - 1].remove();
									frm.call('submit_doc', {
										doctype: "On Duty Application",
										name: d.on_duty_application,
										workflow_state: 'Approved'
									})
										.then(r => {
											frm.get_field("od_approval").grid.grid_rows[d.idx - 1].remove();
										})
								}
								// else if (d.workflow_state == 'Pending for HR') {
								// 	// frappe.db.set_value('On Duty Application', d.on_duty_application, 'workflow_state', 'Approved')
								// 	// frm.get_field("od_approval").grid.grid_rows[d.idx - 1].remove();
								// 	frm.call('submit_doc', {
								// 		doctype: "On Duty Application",
								// 		name: d.on_duty_application,
								// 		workflow_state: 'Approved'
								// 	})
								// 	.then(r => {
								// 		frm.get_field("od_approval").grid.grid_rows[d.idx - 1].remove();
								// 	})
								// }
							}
							else {
								if (d.workflow_state == 'Pending for HOD') {
									frappe.db.set_value('On Duty Application', d.on_duty_application, 'workflow_state', 'Pending for GM')
									frm.get_field("od_approval").grid.grid_rows[d.idx - 1].remove();
								}
								else if (d.workflow_state == 'Pending for GM') {
									frappe.db.set_value('On Duty Application', d.on_duty_application, 'workflow_state', 'Pending for CEO')
									frm.get_field("od_approval").grid.grid_rows[d.idx - 1].remove();
								}
								else if (d.workflow_state == 'Pending for CEO') {
									// frappe.db.set_value('On Duty Application', d.on_duty_application, 'workflow_state', 'Approved')
									// frm.get_field("od_approval").grid.grid_rows[d.idx - 1].remove();
									frm.call('submit_doc', {
										doctype: "On Duty Application",
										name: d.on_duty_application,
										workflow_state: 'Approved'
									}).then(r => {
										frm.get_field("od_approval").grid.grid_rows[d.idx - 1].remove();
									})
								}
							}
						}
					})
				}).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })

			/* OD button end*/

			/* PR button start*/

			frm.fields_dict["pr_approval"].grid.add_custom_button(__('Reject'),
				function () {
					$.each(frm.doc.pr_approval, function (i, d) {
						if (d.__checked == 1) {
							// frappe.db.set_value('Permission Request', d.permission_request, 'workflow_state', 'Rejected')
							frm.call('submit_doc', {
								doctype: "Permission Request",
								name: d.permission_request,
								workflow_state: 'Rejected'
							}).then(r => {
								frm.get_field("pr_approval").grid.grid_rows[d.idx - 1].remove();
							})
							// frm.get_field("pr_approval").grid.grid_rows[d.idx - 1].remove();
						}
					})
				}).addClass('btn-danger')

			frm.fields_dict["pr_approval"].grid.add_custom_button(__('Approve'),
				function () {
					$.each(frm.doc.pr_approval, function (i, d) {
						if (d.__checked == 1) {
							if (d.workflow_state == 'Pending for HOD') {
								// frappe.db.set_value('Permission Request', d.permission_request, 'workflow_state', 'Approved')
								frm.call('submit_doc', {
									doctype: "Permission Request",
									name: d.permission_request,
									workflow_state: 'Approved'
								}).then(r => {
									frm.get_field("pr_approval").grid.grid_rows[d.idx - 1].remove();
								})
							}
						}
					})
				}).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })

			/* PR button end*/

			/* LA button start*/

			frm.fields_dict["la_approval"].grid.add_custom_button(__('Reject'),
				function () {
					$.each(frm.doc.la_approval, function (i, d) {
						if (d.__checked == 1) {
							// frappe.db.set_value('Leave Application', d.leave_application, 'workflow_state', 'Rejected')
							// frm.get_field("la_approval").grid.grid_rows[d.idx - 1].remove();
							frm.call('submit_doc', {
								doctype: "Leave Application",
								name: d.leave_application,
								workflow_state: 'Rejected'
							}).then(r => {
								frm.get_field("la_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
					})
				}).addClass('btn-danger')

			frm.fields_dict["la_approval"].grid.add_custom_button(__('Approve'),
				function () {
					$.each(frm.doc.la_approval, function (i, d) {
						if (d.__checked == 1) {
							if (d.workflow_state == 'Pending for HOD') {
								// frappe.db.set_value('Leave Application', d.leave_application, 'workflow_state', 'Approved')
								// frm.get_field("la_approval").grid.grid_rows[d.idx - 1].remove();
								frm.refresh_field('la_approval')
								frm.call('submit_doc', {
									doctype: "Leave Application",
									name: d.leave_application,
									workflow_state: 'Approved'
								}).then(r => {
									frm.get_field("la_approval").grid.grid_rows[d.idx - 1].remove();
								})
							}
						}
					})
				}).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })

			/* LA button end*/

			/* OT button start*/

			frm.fields_dict["ot_approval"].grid.add_custom_button(__('Reject'),
				function () {
					$.each(frm.doc.ot_approval, function (i, d) {
						if (d.__checked == 1) {
							// frappe.db.set_value('Overtime Request', d.overtime_request, 'workflow_state', 'Rejected')
							frm.call('submit_doc', {
								doctype: "Overtime Request",
								name: d.overtime_request,
								workflow_state: 'Rejected'
							}).then(r => {
								frm.get_field("ot_approval").grid.grid_rows[d.idx - 1].remove();
							})

							// frm.get_field("ot_approval").grid.grid_rows[d.idx - 1].remove();
						}
					})
				}).addClass('btn-danger')

			frm.fields_dict["ot_approval"].grid.add_custom_button(__('Approve'),
				function () {
					$.each(frm.doc.ot_approval, function (i, d) {
						// console.log("HI")
						if (d.__checked == 1) {
							// console.log("HI")
							if (d.workflow_state == 'Pending for HOD') {
								console.log("HI")
								// frappe.db.set_value('Overtime Request', d.overtime_request, 'workflow_state', 'Approved')
								frm.call('submit_doc', {
									doctype: "Overtime Request",
									name: d.overtime_request,
									workflow_state: 'Approved'
								}).then(r => {
									// console.log("HI")
									frm.get_field("ot_approval").grid.grid_rows[d.idx - 1].remove();
								})
								// frm.get_field("ot_approval").grid.grid_rows[d.idx - 1].remove();
							}
						}
					})
				}).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })

			/* OT button end*/

			/* MP button start*/

			frm.fields_dict["mp_approval"].grid.add_custom_button(__('Reject'),
				function () {
					$.each(frm.doc.mp_approval, function (i, d) {
						if (d.__checked == 1) {
							frm.call('submit_doc', {
								doctype: "Miss Punch Application",
								name: d.miss_punch_application,
								workflow_state: 'Rejected'
							}).then(r => {
								frm.get_field("mp_approval").grid.grid_rows[d.idx - 1].remove();
							})
							// frm.get_field("mp_approval").grid.grid_rows[d.idx - 1].remove();
						}
					})
				}).addClass('btn-danger')

			frm.fields_dict["mp_approval"].grid.add_custom_button(__('Approve'),
				function () {
					$.each(frm.doc.mp_approval, function (i, d) {
						if (d.__checked == 1) {
							if (d.workflow_state == 'Pending for HOD') {
								frappe.db.set_value('Miss Punch Application', d.miss_punch_application, 'workflow_state', 'Pending for HR GM')
								frm.get_field("mp_approval").grid.grid_rows[d.idx - 1].remove();
							}
							if (d.workflow_state == "Pending for HR GM") {
								frm.call('submit_doc', {
									doctype: "Miss Punch Application",
									name: d.miss_punch_application,
									workflow_state: 'Approved'
								}).then(r => {
									frm.get_field("mp_approval").grid.grid_rows[d.idx - 1].remove();
								})
								// frm.get_field("mp_approval").grid.grid_rows[d.idx - 1].remove();
							}
						}
					})
				}).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })

			/* MP button end*/
			
			/*Guest Entry Button Start*/

			frm.fields_dict["guest_entry_approval"].grid.add_custom_button(__('Reject'),
				function () {
					$.each(frm.doc.guest_entry_approval, function (i, d) {
						if (d.__checked == 1) {
							frm.call('submit_doc', {
								doctype: "Guest Entry",
								name: d.guest_entry,
								workflow_state: 'Rejected'
							}).then(r => {
								frm.get_field("guest_entry_approval").grid.grid_rows[d.idx - 1].remove();
							})
							frm.get_field("guest_entry_approval").grid.grid_rows[d.idx - 1].remove();
						}
					})
				}).addClass('btn-danger')

			frm.fields_dict["guest_entry_approval"].grid.add_custom_button(__('Approve'),
				function () {
					$.each(frm.doc.guest_entry_approval, function (i, d) {
						if (d.__checked == 1) {
							if (d.workflow_state == 'Pending for HOD') {
								frappe.db.set_value('Guest Entry', d.miss_punch_application, 'workflow_state', 'Pending for HR GM')
								frm.get_field("guest_entry_approval").grid.grid_rows[d.idx - 1].remove();
							}
							if (d.workflow_state == "Pending for HR GM") {
								frm.call('submit_doc', {
									doctype: "Guest Entry",
									name: d.guest_entry,
									workflow_state: 'Approved'
								}).then(r => {
									frm.get_field("guest_entry_approval").grid.grid_rows[d.idx - 1].remove();
								})
								frm.get_field("guest_entry_approval").grid.grid_rows[d.idx - 1].remove();
							}
						}
					})
				}).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })


		}


		/* OD fetch start*/

		var workflow_state = ''
		if (frappe.user.has_role('GM')) {
			console.log('hello')
			workflow_state = ['Pending for HOD', 'Pending for GM']
		}
		else if (frappe.user.has_role('HOD')) {
			workflow_state = ['Pending for HOD']
		}
		else if (frappe.user.has_role('CEO')) {
			workflow_state = ['Pending for CEO']
		}
		else if (frappe.user.has_role('HR')) {
			workflow_state = ['Pending for HR']
		}
		frappe.db.get_value('Employee', { 'user_id': frappe.session.user }, 'name', r => {

		frappe.call({
			"method": "frappe.client.get_list",
			"args": {
				"doctype": "On Duty Application",
				"filters": [
					['workflow_state', 'in', workflow_state],
					['employee', '!=', r.name,]
				],
				limit_page_length: 500
			},
			callback(r) {
				$.each(r.message, function (i, d) {
					frappe.call({
						"method": "frappe.client.get",
						"args": {
							"doctype": "On Duty Application",
							"name": d.name
						},
						callback(r) {
							frm.add_child('od_approval', {
								'on_duty_application': r.message.name,
								'employee_id': r.message.employee,
								'employee_name': r.message.employee_name,
								'department': r.message.department,
								'workflow_state': r.message.workflow_state,
								'from_date': r.message.from_date,
								'to_date': r.message.to_date,
								'from_time': r.message.from_time,
								'to_time': r.message.to_time,
								'vehicle_request': r.message.vehicle_request,
								'session': r.message.from_date_session,
								'address': r.message.address,
								'person_to_meet': r.message.person_to_meet,
								'company_name': r.message.company_name,
								'purpose': r.message.description
							})
							frm.refresh_field('od_approval')
						}
					})

				})
			}
		})
	})
		/* OD fetch end*/

		/* PR fetch start*/
		// if (frappe.user.has_role(['HOD', 'GM'])) {
		// frappe.call({
		// 	"method": "frappe.client.get_value",
		// 	"args": {
		// 		"doctype": "Employee",
		// 		"filters": {
		// 			'user_id': frappe.session.user
		// 		},
		// 		"fieldname": 'name'
		// 	},
		// 	callback(r){
		// 		var emp = r.message.name
		// 	}
		// })
		frappe.db.get_value('Employee', { 'user_id': frappe.session.user }, 'name', r => {

			frappe.call({
				"method": "frappe.client.get_list",
				"args": {
					"doctype": "Permission Request",
					"filters": [
						['workflow_state', '=', 'Pending for HOD'],
						['employee', '!=', r.name,]
					],
					limit_page_length: 500
				},
				callback(r) {
					$.each(r.message, function (i, d) {
						frappe.call({
							"method": "frappe.client.get",
							"args": {
								"doctype": "Permission Request",
								"name": d.name
							},
							callback(r) {
								frm.add_child('pr_approval', {
									'permission_request': r.message.name,
									'employee': r.message.employee,
									'employee_name': r.message.employee_name,
									'workflow_state': r.message.workflow_state,
									'requested_date': r.message.requested_date,
									'department': r.message.department,
									'designation': r.message.designation,
									'permission_approver': r.message.permission_approver,
									'permission_approver_name': r.message.permission_approver_name,
									'attendance_date': r.message.attendance_date,
									'shift': r.message.shift,
									'reason': r.message.reason,
									'session': r.message.session,
									'from_time': r.message.from_time,
									'to_time': r.message.to_time,
									'hours': r.message.hours

								})
								frm.refresh_field('pr_approval')
							}
						})

					})
				}
			})
		})
		// }
		/* PR fetch end*/

		/* LA fetch start*/
		// if (frappe.user.has_role(['HOD', 'GM'])) {
		frappe.db.get_value('Employee', { 'user_id': frappe.session.user }, 'name', r => {
			frappe.call({
				"method": "frappe.client.get_list",
				"args": {
					"doctype": "Leave Application",
					"filters": [
						['workflow_state', '=', 'Pending for HOD'],
						['employee', '!=', r.name,]
					],
					limit_page_length: 500
				},
				callback(r) {
					$.each(r.message, function (i, d) {
						frappe.call({
							"method": "frappe.client.get",
							"args": {
								"doctype": "Leave Application",
								"name": d.name
							},
							callback(r) {
								frm.add_child('la_approval', {
									'leave_application': r.message.name,
									'employee': r.message.employee,
									'employee_name': r.message.employee_name,
									'workflow_state': r.message.workflow_state,
									'request_date': r.message.request_date,
									'department': r.message.department,
									'leave_type': r.message.leave_type,
									'leave_balance': r.message.leave_balance,
									'from_date': r.message.from_date,
									'from_date': r.message.from_date,
									'half_day': r.message.half_day,
									'half_day_date': r.message.half_day_date,
									'total_leave_days': r.message.total_leave_days,
									'session': r.message.session,
									'description': r.message.to_time,
									'leave_approver': r.message.leave_approver,
									'leave_approver_name': r.message.leave_approver_name
								})
								frm.refresh_field('la_approval')
							}
						})

					})
				}
			})
		})
		// }
		/* LA fetch end*/

		/* OT fetch start*/
		// if (frappe.user.has_role(['HOD', 'GM'])) {
		frappe.db.get_value('Employee', { 'user_id': frappe.session.user }, 'name', r => {
			frappe.call({
				"method": "frappe.client.get_list",
				"args": {
					"doctype": "Overtime Request",
					"filters": [
						['workflow_state', '=', 'Pending for HOD'],
						['employee', '!=', r.name]
					],
					limit_page_length: 500
				},
				callback(r) {
					$.each(r.message, function (i, d) {
						frappe.call({
							"method": "frappe.client.get",
							"args": {
								"doctype": "Overtime Request",
								"name": d.name
							},
							callback(r) {
								if (r.message.ot_hours != '0:00:00' ){
									// console.log(r.message.ot_hours)
									frm.add_child('ot_approval', {
										'overtime_request': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'workflow_state': r.message.workflow_state,
										'ot_date': r.message.ot_date,
										'department': r.message.department,
										'shift': r.message.shift,
										'from_time': r.message.from_time,
										'to_time': r.message.to_time,
										'total_hours': r.message.total_hours,
										'ot_hours': r.message.ot_hours,
										'bio_in': r.message.bio_in,
										'bio_out': r.message.bio_out,
										'total_wh': r.message.total_wh,
										'approver': r.message.approver,
										'approver_id': r.message.approver_id,
										'approver_name': r.message.approver_name
									})
									frm.refresh_field('ot_approval')
								}
							}
						})

					})
				}
			})
		})
		// }
		/* OT fetch end*/

		/* MP fetch start*/
		frappe.db.get_value('Employee', { 'user_id': frappe.session.user }, 'name', r => {
			frappe.call({
				"method": "frappe.client.get_list",
				"args": {
					"doctype": "Miss Punch Application",
					"filters": [
						['workflow_state', 'in', ['Pending for HOD', 'Pending for HR GM']],
						['employee', '!=', r.name]
					],
					limit_page_length: 500
				},
				callback(r) {
					$.each(r.message, function (i, d) {
						frappe.call({
							"method": "frappe.client.get",
							"args": {
								"doctype": "Miss Punch Application",
								"name": d.name
							},
							callback(r) {
								frm.add_child('mp_approval', {
									'miss_punch_application': r.message.name,
									'employee': r.message.employee,
									'employee_name': r.message.employee_name,
									'department': r.message.department,
									'workflow_state': r.message.workflow_state,
									'attendance_date': r.message.attendance_date,
									'attendance': r.message.attendance,
									'in_time': r.message.in_time,
									'out_time': r.message.out_time,
									'qr_shift': r.message.qr_shift
								})
								frm.refresh_field('mp_approval')
							}
						})

					})
				}
			})
		})
		if (frappe.session.user == 'Administrator'){
			frappe.call({
				"method": "frappe.client.get_list",
				"args": {
					"doctype": "Miss Punch Application",
					"filters": [
						['workflow_state', 'in', ['Pending for HOD', 'Pending for HR GM']],
						['employee', '!=', r.name]
					],
					limit_page_length: 500
				},
				callback(r) {
					$.each(r.message, function (i, d) {
						frappe.call({
							"method": "frappe.client.get",
							"args": {
								"doctype": "Miss Punch Application",
								"name": d.name
							},
							callback(r) {
								frm.add_child('mp_approval', {
									'miss_punch_application': r.message.name,
									'employee': r.message.employee,
									'employee_name': r.message.employee_name,
									'department': r.message.department,
									'workflow_state': r.message.workflow_state,
									'attendance_date': r.message.attendance_date,
									'attendance': r.message.attendance,
									'in_time': r.message.in_time,
									'out_time': r.message.out_time,
									'qr_shift': r.message.qr_shift
								})
								frm.refresh_field('mp_approval')
							}
						})

					})
				}
			})
		}
		frappe.db.get_value('Employee', { 'user_id': frappe.session.user }, 'name', r => {
			frappe.call({
				"method": "frappe.client.get_list",
				"args": {
					"doctype": "Guest Entry",
					"filters": [
						['workflow_state', '=', 'Pending for HOD'],
						['employee', '!=', r.name]
					],
					limit_page_length: 500
				},
				callback(r) {
					$.each(r.message, function (i, d) {
						frappe.call({
							"method": "frappe.client.get",
							"args": {
								"doctype": "Guest Entry",
								"name": d.name
							},
							callback(r) {
								frm.add_child('guest_entry_approval', {
									'from_date': r.message.from,
									'to_sate': r.message.to,
									'requster_id': r.message.requester_id,
									'workflow_state': r.message.workflow_state,
									'guest_id': r.message.name,
									'party_name': r.message.party_name,
								})
								frm.refresh_field('guest_entry_approval')
							}
						})

					})
				}
			})
		})
		/* Guest fetch end*/
	},
	od_approval_on_form_rendered: function (frm, cdt, cdn) {
		frm.fields_dict['od_approval'].grid.wrapper.find('.grid-delete-row').hide();
		frm.fields_dict['od_approval'].grid.wrapper.find('.grid-duplicate-row').hide();
		frm.fields_dict['od_approval'].grid.wrapper.find('.grid-move-row').hide();
		frm.fields_dict['od_approval'].grid.wrapper.find('.grid-append-row').hide();
		frm.fields_dict['od_approval'].grid.wrapper.find('.grid-insert-row-below').hide();
		frm.fields_dict['od_approval'].grid.wrapper.find('.grid-insert-row').hide();
	},
	pr_approval_on_form_rendered: function (frm, cdt, cdn) {
		frm.fields_dict['pr_approval'].grid.wrapper.find('.grid-delete-row').hide();
		frm.fields_dict['pr_approval'].grid.wrapper.find('.grid-duplicate-row').hide();
		frm.fields_dict['pr_approval'].grid.wrapper.find('.grid-move-row').hide();
		frm.fields_dict['pr_approval'].grid.wrapper.find('.grid-append-row').hide();
		frm.fields_dict['pr_approval'].grid.wrapper.find('.grid-insert-row-below').hide();
		frm.fields_dict['pr_approval'].grid.wrapper.find('.grid-insert-row').hide();
	},
	la_approval_on_form_rendered: function (frm, cdt, cdn) {
		frm.fields_dict['la_approval'].grid.wrapper.find('.grid-delete-row').hide();
		frm.fields_dict['la_approval'].grid.wrapper.find('.grid-duplicate-row').hide();
		frm.fields_dict['la_approval'].grid.wrapper.find('.grid-move-row').hide();
		frm.fields_dict['la_approval'].grid.wrapper.find('.grid-append-row').hide();
		frm.fields_dict['la_approval'].grid.wrapper.find('.grid-insert-row-below').hide();
		frm.fields_dict['la_approval'].grid.wrapper.find('.grid-insert-row').hide();
	},
	ot_approval_on_form_rendered: function (frm, cdt, cdn) {
		frm.fields_dict['ot_approval'].grid.wrapper.find('.grid-delete-row').hide();
		frm.fields_dict['ot_approval'].grid.wrapper.find('.grid-duplicate-row').hide();
		frm.fields_dict['ot_approval'].grid.wrapper.find('.grid-move-row').hide();
		frm.fields_dict['ot_approval'].grid.wrapper.find('.grid-append-row').hide();
		frm.fields_dict['ot_approval'].grid.wrapper.find('.grid-insert-row-below').hide();
		frm.fields_dict['ot_approval'].grid.wrapper.find('.grid-insert-row').hide();
	},
	mp_approval_on_form_rendered: function (frm, cdt, cdn) {
		frm.fields_dict['mp_approval'].grid.wrapper.find('.grid-delete-row').hide();
		frm.fields_dict['mp_approval'].grid.wrapper.find('.grid-duplicate-row').hide();
		frm.fields_dict['mp_approval'].grid.wrapper.find('.grid-move-row').hide();
		frm.fields_dict['mp_approval'].grid.wrapper.find('.grid-append-row').hide();
		frm.fields_dict['mp_approval'].grid.wrapper.find('.grid-insert-row-below').hide();
		frm.fields_dict['mp_approval'].grid.wrapper.find('.grid-insert-row').hide();
	},
	guest_entry_approval_on_form_rendered: function (frm, cdt, cdn) {
		frm.fields_dict['guest_entry_approval'].grid.wrapper.find('.grid-delete-row').hide();
		frm.fields_dict['guest_entry_approval'].grid.wrapper.find('.grid-duplicate-row').hide();
		frm.fields_dict['guest_entry_approval'].grid.wrapper.find('.grid-move-row').hide();
		frm.fields_dict['guest_entry_approval'].grid.wrapper.find('.grid-append-row').hide();
		frm.fields_dict['guest_entry_approval'].grid.wrapper.find('.grid-insert-row-below').hide();
		frm.fields_dict['guest_entry_approval'].grid.wrapper.find('.grid-insert-row').hide();
	},
});
