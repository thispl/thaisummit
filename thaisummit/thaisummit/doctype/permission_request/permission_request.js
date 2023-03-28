// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Permission Request', {
	refresh: function (frm) {
		frappe.breadcrumbs.add("HR", "Permission Request");
		// 		if (frappe.user.has_role("HOD")) {
		// 		if(!frm.is_new()){
		// 			if(frm.doc.status == "Applied"){
		// 		frm.add_custom_button(__("Approve"), function(){
		// 			frm.call('submit_doc').then((d)=>{
		// 				if(d.message == "ok"){
		// 				frm.refresh()
		// 				}
		// 			})
		// 		  }).css({'background-color':'#00FF00' });
		// 		}
		// 	}
		// }
	},
	employee(frm) {
		if (frm.doc.employee) {
			frappe.call({
				"method": "thaisummit.custom.get_approver",
				"args": {
					"employee": frm.doc.employee,
					"department": frm.doc.department
				},
				callback(r) {
					frm.set_value('permission_approver', r.message)
					
				}
			})
		}
		// if (frm.doc.employee){

		// if (frappe.user.has_role('GM')){
		// frm.call('get_ceo').then(r=>{
		// console.log('gm')
		// 	frm.set_value('permission_approver',r.message)
		// })
		// }
		// else if (frappe.user.has_role('HOD')){
		// console.log('hod')
		// 	frm.call('get_gm').then(r=>{
		// 		frm.set_value('permission_approver',r.message)
		// 	})
		// }
		// else {
		// 	frm.call('get_hod').then(r=>{
		// 		frm.set_value('permission_approver',r.message)
		// 	})
		// 	}

		// }
	},
	attendance_date(frm) {
		if (!frappe.user.has_role('HR GM')) {
			if (frm.doc.attendance_date) {
				var date = frappe.datetime.add_days(frm.doc.attendance_date, 3)
				frappe.call({
					"method":"thaisummit.utils.get_server_date" ,
					callback(r){
						if (r.message > date) {
							frappe.msgprint("Permission should be applied within 3 days")
							frappe.validated = false;
						}
					}
				})
			}
		}
		// if(frm.doc.attendance_date){
		// 	frappe.call({
		// 		method : 'thaisummit.custom.application_allowed_from',
		// 		args:{
		// 			date : frm.doc.attendance_date
		// 		},
		// 		callback(r){
		// 			if (r.message == 'NO'){
		// 				frm.set_value('attendance_date','')
		// 			}
		// 		}
		// 	})
		// }
	},
	validate(frm) {
		if (!frappe.user.has_role('HR GM')) {
			if (frm.doc.attendance_date) {
				var date = frappe.datetime.add_days(frm.doc.attendance_date, 3)
				frappe.call({
					"method":"thaisummit.utils.get_server_date" ,
					callback(r){
						if (r.message > date) {
							frappe.msgprint("Permission should be applied within 3 days")
							frappe.validated = false;
						}
					}
				})
			}
		}
	},
	after_save(frm){
		console.log('ok')
		
	},
	shift(frm) {
		if (frm.doc.shift) {
			frappe.call({
				"method": "frappe.client.get",
				"args": {
					doctype: "Shift Type",
					filters: {
						name: frm.doc.shift
					},
					fieldname: ["name", "start_time", "end_time"]
				},
				callback(r) {
					frm.set_value("session", 'First Half')
					frm.set_value("from_time", r.message.start_time)
					frm.call('get_endtime1', {
						start_time: r.message.start_time
					}).then((d) => {
						frm.set_value("to_time", d.message)
					})
				}
			})
		}
	},
	session(frm) {
		if (frm.doc.shift) {
			if (frm.doc.session == 'Second Half') {
				frappe.call({
					"method": "frappe.client.get",
					"args": {
						doctype: "Shift Type",
						filters: {
							name: frm.doc.shift
						},
						fieldname: ["name", "start_time", "end_time"],
					},
					callback(r) {
						frm.set_value("to_time", r.message.end_time)
						frm.call('get_endtime2', {
							end_time: r.message.end_time
						}).then((d) => {
							frm.set_value("from_time", d.message)
						})
					}
				})
			}
			else {
				frm.trigger('shift')
			}
		}
	}
});
