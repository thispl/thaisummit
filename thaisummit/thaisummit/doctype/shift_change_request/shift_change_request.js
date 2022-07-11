// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shift Change Request', {
	attendance_date:function(frm) {
		if (frm.doc.__islocal){
			frappe.call({
				'method':'frappe.client.get_value',
				'args':{
					'doctype':'Shift Assignment',
					'filters':{
						'employee':frm.doc.employee,
						'start_date':frm.doc.attendance_date,

					},
					'fieldname':['shift_type','name']
				},
				callback(r){
					if(r.message){	
						frm.set_value('actual_shift',r.message.shift_type)
						frm.set_value('shift_marked',r.message.name)	
					}
				}
			})
		}
	},
});
