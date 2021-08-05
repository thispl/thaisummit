// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Overtime Request', {
	refresh: function (frm) {
		frappe.breadcrumbs.add("HR", "Overtime Request");
		if (frm.doc.__islocal) {
			frappe.call({
				method: 'thaisummit.custom.get_employee_code',
				args: {
					user: frappe.session.user
				},
				callback(r) {
					if (r.message) {
						frm.set_value('employee', r.message)
						// if (!frm.doc.approver) {
						// 	if (frappe.user.has_role('GM')) {
						// 		frm.call('get_ceo', { employee: r.message }).then(r => {
						// 			frm.set_value('approver_id', r.message)
						// 		})
						// 	}
						// 	else if (frappe.user.has_role('HOD')) {
						// 		frm.call('get_gm', { employee: r.message }).then(r => {
						// 			frm.set_value('approver_id', r.message)
						// 		})
						// 	}
						// 	else {
						// 		frm.call('get_hod', { employee: r.message }).then(r => {
						// 			frm.set_value('approver_id', r.message)
						// 		})
						// 	}
						// }
					}
				}
			})
		}
	},
	after_save(frm) {
		frm.call('send_for_approval')
	},
	validate(frm) {
		if (!frm.doc.employee) {
			frappe.throw("Please enter Employee ID")
		}
		if (!frm.doc.ot_date) {
			frappe.throw("Please enter OT Date")
		}
		if (!frm.doc.shift) {
			frappe.throw("Please enter Shift")
		}
		if (!frm.doc.from_time) {
			frappe.throw("Please enter From Time")
		}
		if (!frm.doc.to_time) {
			frappe.throw("Please enter To Time")
		}
	},
	employee(frm) {
		if (frm.doc.employee) {
			if (!frm.doc.approver) {
				if (frappe.user.has_role('GM')) {
					frm.call('get_ceo', { employee: frm.doc.employee }).then(r => {
						frm.set_value('approver_id', r.message)
					})
				}
				else if (frappe.user.has_role('HOD')) {
					frm.call('get_gm', { employee: frm.doc.employee }).then(r => {
						frm.set_value('approver_id', r.message)
					})
				}
				else {
					frm.call('get_hod', { employee: frm.doc.employee }).then(r => {
						frm.set_value('approver_id', r.message)
					})
				}
				// frappe.call({
				// 	"method": "frappe.client.get",
				// 	args: {
				// 		doctype: "Employee",
				// 		filters: { "user_id": frm.doc.approver },
				// 		fieldname: ["name", "employee_name"]
				// 	},
				// 	callback(r) {
				// 		if (r.message.name) {
				// 			frm.set_value('approver_id', r.message.name)
				// 			frm.set_value('approver_name', r.message.employee_name)
				// 		}
				// 		else {
				// 			frm.set_value('approver_id', '')
				// 			frm.set_value('approver_name', '')
				// 		}
				// 	}
				// })
			} 
			// else {
			// 	frm.set_value('approver_id', '')
			// 	frm.set_value('approver_name', '')
			// }
		}
	},
	shift(frm) {
		if (frm.doc.ot_date) {
			if (frm.doc.shift) {
				if(frm.doc.shift == '1'){
					frm.call('check_holiday').then(r=>{
						if(r.message == 'NO'){
							frappe.msgprint("Overtime Request for Shift 1 can be applied only on Sunday or Holiday")
							frm.set_value('from_time','')
						}
						else{
							frappe.db.get_value('Shift Type', frm.doc.shift, 'start_time', (r) => {
								frm.set_value('from_time', r.start_time)
								frm.set_value('to_time', '')
								frm.set_value('ot_hours', '')
								frm.set_value('total_hours', '')
							})
						}
					})
				}
				else{
					frappe.db.get_value('Shift Type', frm.doc.shift, 'start_time', (r) => {
						frm.set_value('from_time', r.start_time)
						frm.set_value('to_time', '')
						frm.set_value('ot_hours', '')
						frm.set_value('total_hours', '')
					})
				}
				
			}
			
		}
		else{
			frappe.throw("Please enter Shift")
		}
	},
	from_time(frm) {
		if (frm.doc.from_time) {
			frappe.call({
				method: 'thaisummit.custom.roundoff_time',
				args: {
					time: frm.doc.from_time
				},
				callback(r) {
					if (r.message) {
						frm.set_value('from_time', r.message)
						frm.call('check_shift_time')
					}
				}
			})
		}
		frm.trigger('to_time')
	},
	to_time(frm){
		if(frm.doc.to_time){
			frappe.call({
				method:'thaisummit.custom.roundoff_time',
				args:{
					time : frm.doc.to_time
				},
				callback(r){
					if(r.message){
						frm.set_value('to_time',r.message)
					}
				}
			})
		}
		if (frm.doc.from_time && frm.doc.to_time) {
			frappe.call({
				"method": "thaisummit.thaisummit.doctype.overtime_request.overtime_request.ot_hours",
				args: {
					'ot_date': frm.doc.ot_date,
					'shift': frm.doc.shift,
					'from_time': frm.doc.from_time,
					"to_time": frm.doc.to_time,
				},
				callback(r) {
					frm.set_value('ot_hours', r.message[1])
					frm.set_value('total_hours', r.message[0])
				}
			})
		}
	},
	ot_date(frm) {
		if(frm.doc.shift){
			frm.trigger('shift')
		}
		if (frm.doc.ot_date) {
			frm.call('get_bio_checkins')
		}
		if (frm.doc.ot_date) {
			frappe.call({
				method: 'thaisummit.custom.application_allowed_from',
				args: {
					date: frm.doc.ot_date
				},
				callback(r) {
					if (r.message == 'NO') {
						frm.set_value('ot_date', '')
					}
				}
			})
		}
	}
});