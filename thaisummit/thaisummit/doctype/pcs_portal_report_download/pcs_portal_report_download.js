// Copyright (c) 2023, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('PCS Portal Report Download', {
	refresh: function(frm) {
		frm.disable_save()
	},
	download: function (frm) {
		frm.call('create_new_doc').then(r => {

		})
		var path = "thaisummit.thaisummit.doctype.pcs_portal_report_download.pcs_portal_report.download"
		var args = 'customer=%(customer)s'
		if (path) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path,
				args: args,
				customer : frm.doc.customer
			});
		}
		frm.save()
	}
});
