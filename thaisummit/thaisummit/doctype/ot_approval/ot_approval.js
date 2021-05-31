// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('OT Approval', {
	refresh: function(frm) {
		frappe.breadcrumbs.add("HR","OT Approval");
        frm.disable_save()
		frm.fields_dict['ot_approval'].grid.wrapper.find('.grid-add-row').hide();
		frm.set_value("from_date", frappe.datetime.month_start());
		frm.set_value("to_date", frappe.datetime.month_end());
		frappe.model.clear_table(frm.doc, "ot_approval");
		frm.call('get_default_data')
		.then(r =>{
			console.log(r.message)
			refresh_field("ot_approval")
		})


	},
	onload:function(frm){
		$(".grid-add-row").hide();
	},
	to_date:function(frm){
		// if (frm.doc.employee_id){
		frappe.model.clear_table(frm.doc, "ot_approval");
		frm.call('get_data_datewise')
		.then(r =>{
			console.log(r.message)
			// frm.save()
			refresh_field("ot_approval")
		})
		refresh_field("ot_approval")
	},
	employee_id:function(frm){
		if (frm.doc.employee_id){
		frappe.model.clear_table(frm.doc, "ot_approval");
			frm.call('get_data_id')
			.then(r =>{
				console.log(r.message)
				refresh_field("ot_approval")
				// frm.save()				
			})
			refresh_field("ot_approval")
		}
		else {
			frm.set_value("employee_name","")
			frappe.model.clear_table(frm.doc, "ot_approval");
			// refresh_field("ot_approval")
			// frm.save()
			
		}
	}
});
frappe.ui.form.on("OT Table", "submit", function(frm, cdt, cdn) {
	var child =locals[cdt][cdn]
	console.log(child.ot_hours)
	if(child.ot_hours){
	frm.call('update_attendance', {
		row: child,
	}).then(r =>{
		frm.get_field("ot_approval").grid.grid_rows[child.idx - 1].remove();
		frappe.msgprint("OT hours is updated")
	})
	}
	else{
		frappe.msgprint("Please enter OT hours")
	}
});