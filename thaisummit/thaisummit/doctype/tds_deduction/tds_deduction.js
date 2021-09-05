// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('TDS Deduction', {
	refresh: function(frm) {
		if (frm.doc.__islocal){
		frm.call('get_payroll_date')
		}
	},
});
