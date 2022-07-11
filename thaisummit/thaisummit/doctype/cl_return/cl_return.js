// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('CL Return', {

	//This is the employee_id field to get employee details from EMP MIS and to set the details in Child table
	employee_id:function(frm){
		if(frm.doc.employee_id){
			var emp = frappe.db.get_doc('Employee',frm.doc.employee_id)
			.then(doc => {
				frm.add_child('cl_returns_entry',{
					employee_id:frm.doc.employee_id,
					employee_name:doc.employee_name,
					department:doc.department,
				}),
				frm.set_value('employee_id','')
				frm.refresh_field("cl_returns_entry")
			
			})


		}
	},
	//This is the submit button, while submit action create a new doc of CL Return Form of Each Employee
	submit(frm){
		frm.call('new_cl_return_form')
            .then(r => {
			frm.set_value("cl_returns_entry", [])
		})
		
		
	},
	// this is the doctype to disable the save function
	refresh: function (frm) {
		frm.set_value('date', frappe.datetime.get_today())
		var time = new Date().toLocaleTimeString();
	    var time_format = moment(time, "h:mm:ss A").format("HH:mm");  
	    frm.set_value('time',time_format)
        frm.disable_save()
		frm.set_value("cl_returns_entry", [])	

    },
});
