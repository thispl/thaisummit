// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('CL Return Form', {
	refresh: function(frm) {
		var time = new Date().toLocaleTimeString();
	    var time_format = moment(time, "h:mm:ss A").format("HH:mm");  
	    frm.set_value('time',time_format)

	}
});
