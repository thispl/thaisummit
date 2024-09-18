// Copyright (c) 2023, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Checkin Log', {
	refresh: function(frm) {
		frm.add_custom_button(__("Process Checkins"), function(){
			frm.call('process_checkin_log')
		  })
	}
});
