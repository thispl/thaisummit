// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Manpower Attendance Report', {

	download(frm) {
		window.open(
			frappe.urllib.get_full_url(`/api/method/frappe.utils.print_format.download_pdf?
						doctype=${encodeURIComponent("Manpower Attendance Report")}
						&name=${encodeURIComponent(frm.doc.name)}
						&format=${encodeURIComponent('Manpower Attendance Report')}`)
		);
	}
});
