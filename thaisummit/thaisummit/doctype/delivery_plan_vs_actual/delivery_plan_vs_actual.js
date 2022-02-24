// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Delivery Plan vs Actual', {
	// refresh: function(frm) {

	// }
	download: function (frm) {
		
			if (frm.doc.from_date && frm.doc.to_date ){
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: "thaisummit.thaisummit.doctype.delivery_plan_vs_actual.delivery_plan_vs_actual.download",
				args: 'from_date=%(from_date)s&to_date=%(to_date)s',
				from_date : frm.doc.from_date,
				to_date : frm.doc.to_date,
				
			});
		}else{
			frappe.throw('Please Enter From Date and To Date')
		}
		
	},
});
