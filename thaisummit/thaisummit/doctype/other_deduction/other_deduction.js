// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Other Deduction', {
	refresh: function(frm) {
		frappe.breadcrumbs.add("Home", "Other Deduction");
		if (frm.doc.__islocal){
		frm.set_value('deduction_date',frappe.datetime.nowdate())
		}
	},
	deduction_date(frm){
		frm.call('get_payroll_date')
	},

});
