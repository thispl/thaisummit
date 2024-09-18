// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('HR Time Settings', {
	update_amount(frm){
		frappe.call({
			"method": "thaisummit.custom.get_ot_amount",
			"args":{
				"from_date" : frm.doc.from_date,
				"to_date" : frm.doc.to_date,
			},
			freeze: true,
			freeze_message: 'Processing Overtime Amount....',
			callback(r){
				console.log(r.message)
				if(r.message == "ok"){
					frappe.msgprint("Overtime Amuount is Updating in the Background. Kindly check after sometime")
				}
			}
		})
	},
});
