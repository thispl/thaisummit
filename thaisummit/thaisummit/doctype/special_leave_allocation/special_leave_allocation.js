// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Special Leave Allocation', {
	refresh: function(frm) {

	},
	employee_id: function(frm) {
		if (frm.doc.employee_id) {
			// console.log("hi")
		// var today = new Date();
        // var date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
		frappe.call({
			
			method: "erpnext.hr.doctype.leave_application.leave_application.get_leave_details",
			args: {
				employee: frm.doc.employee_id,
				date: frm.doc.date
				
			},
			
			callback: function(r) {
				console.log("hi")
				$.each(r.message["leave_allocation"], function (i, d) {
					var row = frappe.model.add_child(frm.doc, "Special allocation table", "special_allocation_table")
					row.leave_type = i
					row.open = d.total_leaves
					row.used = d.leaves_taken
					row.balance = d.remaining_leaves
				})
				refresh_field("special_allocation_table")
			}
	})
	}
	},
	submit:function(frm){
		frm.call('update_leave_allocation',{
			allocation:frm.doc.special_allocation_table
		})
		.then(r =>{
			console.log(r.message)
			// frappe.show_alert(__(r.message), 5);
		})
	}
});
