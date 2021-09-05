// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shift Schedule Status Summary', {
	download(frm){
		window.open(
			frappe.urllib.get_full_url(`/api/method/frappe.utils.print_format.download_pdf?
				doctype=${encodeURIComponent("Shift Schedule Status Summary")}
				&name=${encodeURIComponent(frm.doc.name)}
				&format=${encodeURIComponent('Shift Schedule Status Summary')}`)
		);
	},
	from_date(frm){
		frm.set_value("to_date",frappe.datetime.add_days(frm.doc.from_date,5))
	}
});
