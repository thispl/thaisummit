// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Monthly Sales Per Head', {
	// refresh: function(frm) {

	// }
	download(frm) {
		window.open(
			frappe.urllib.get_full_url(`/api/method/frappe.utils.print_format.download_pdf?
						doctype=${encodeURIComponent("Monthly Sales Per Head")}
						&name=${encodeURIComponent(frm.doc.name)}
						&format=${encodeURIComponent('Monthly Sales Per Head')}`)
		);
	}
});
