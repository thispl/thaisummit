// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('TSAI Invoice', {
	onload(frm) {
        var time = new Date().toLocaleTimeString();
        var time_format = moment(time, "h:mm:ss A").format("HH:mm");
        frm.set_value('invoice_time', time_format)
	}
});
