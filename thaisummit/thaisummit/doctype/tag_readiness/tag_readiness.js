// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tag Readiness', {
	refresh: function (frm) {
        frm.disable_save()
		let slot_no = frappe.route_options.slot_no;
        frm.set_value('slot_no',slot_no);
    },
	submit: function (frm) {
        // cur_frm.set_df_property("submit", "hidden", true);
        // var today = new Date();

        // var date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();

        // var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        // var datetime = date + ' ' + time
        // frm.set_value("submit_time", datetime)
        frm.call('update_readiness')
            .then(r => {
                frappe.show_alert(__(r.message), 5);
                frappe.set_route("List", "TAG Master",{slot_no:frm.doc.slot_no});
            })
    },
	slot_no: function (frm) {
		frappe.db.get_list('TAG Master',
			{ fields: ['*'], filters:{ "slot_no": frm.doc.slot_no } }).then((res) => {
				res.forEach((doc) => {
					frm.add_child("tag_readiness_update", {
						vehicle: doc.vehicle,
						model_number: doc.model_number,
						parts_no: doc.parts_no,
						parts_name: doc.parts_name,
						mat_no: doc.mat_no,
						required_quantity: doc.required_quantity,
						sap_quantity: doc.sap_quantity,
						tag_master: doc.name,
						readiness_qty : doc.required_quantity
					})
					frm.refresh_field("tag_readiness_update")
				});
			});
	}
});

frappe.ui.form.on('Tag Readiness Update', {
	readiness_qty: function (frm,cdt,cdn) {
		var row = locals[cdt][cdn];
		if (parseInt(row.readiness_qty) > parseInt(row.required_quantity)){
			frappe.msgprint("Readiness Qty should not be greater than Required Qty")
			row.readiness_qty = 0
		}
    },});
