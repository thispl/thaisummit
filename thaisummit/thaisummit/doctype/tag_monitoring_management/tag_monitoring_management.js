// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('TAG Monitoring Management', {
	refresh: function(frm) {
        frm.disable_save()
        
    },

	get_item_qty:function(frm){
		frappe.call({
			method: "thaisummit.custom.get_sap_qty",
			freeze: true,
        	freeze_message: 'Updating....',
			callback: function (r) {
				if (r.message) {
					console.log(r.message)
					// frappe.msgprint(__(r.message))
				}
			}
		});

	}

});
