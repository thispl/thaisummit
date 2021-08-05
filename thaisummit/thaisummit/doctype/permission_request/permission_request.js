// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Permission Request', {
	refresh: function(frm) {
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
	employee(frm){
		if (frm.doc.employee){
			if (frappe.user.has_role('GM')){
			frm.call('get_ceo').then(r=>{
				frm.set_value('permission_approver',r.message)
			})
			}
			else if (frappe.user.has_role('HOD')){
				frm.call('get_gm').then(r=>{
					frm.set_value('permission_approver',r.message)
				})
			}
			else {
				frm.call('get_hod').then(r=>{
					frm.set_value('permission_approver',r.message)
				})
				}

		}
	},
	attendance_date(frm){
		if(frm.doc.attendance_date){
			frappe.call({
				method : 'thaisummit.custom.application_allowed_from',
				args:{
					date : frm.doc.attendance_date
				},
				callback(r){
					if (r.message == 'NO'){
						frm.set_value('attendance_date','')
					}
				}
			})
		}
	},
	shift(frm){
		if(frm.doc.shift){
			frappe.call({
				"method": "frappe.client.get",
				"args":{
					doctype: "Shift Type",
					fieldname: ["name","start_time","end_time"],
					filters:{
						name : frm.doc.shift
					}
				},
				callback(r){
					frm.set_value("session",'First Half')
					frm.set_value("from_time",r.message.start_time)
					frm.call('get_endtime1',{
						start_time : r.message.start_time
					}).then((d) => {
						frm.set_value("to_time",d.message)
					})
				}
			})
		}
	},
	session(frm){
		if(frm.doc.shift){
			if(frm.doc.session == 'Second Half'){
			frappe.call({
				"method": "frappe.client.get",
				"args":{
					doctype: "Shift Type",
					fieldname: ["name","start_time","end_time"],
					filters:{
						name : frm.doc.shift
					}
				},
				callback(r){
					frm.set_value("to_time",r.message.end_time)
					frm.call('get_endtime2',{
						end_time : r.message.end_time
					}).then((d) => {
						frm.set_value("from_time",d.message)
					})
				}
			})
		}
		else{
			frm.trigger('shift')
		}
		}
	}
});
