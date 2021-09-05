// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt



frappe.ui.form.on('Other Allowance', {
	refresh: function(frm) {
		if (frm.doc.__islocal){
		frm.set_value('allowance_date',frappe.datetime.nowdate())
		}
	},
	allowance_date(frm){
		frm.call('get_payroll_date')
	},
});
