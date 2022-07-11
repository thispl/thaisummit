// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Invoice GRN Detail', {
	refresh: function (frm) {
		frm.disable_save()
	},
	download: function (frm) {
		window.location.href = repl(frappe.request.url +
			'?cmd=%(cmd)s&supplier=%(supplier)s&from_date=%(from_date)s&to_date=%(to_date)s', {
			cmd: "thaisummit.thaisummit.doctype.invoice_grn_detail.invoice_grn_detail.download",
			supplier: frm.doc.supplier || '',
			from_date: frm.doc.from_date,
			to_date: frm.doc.to_date
		});
	},
});