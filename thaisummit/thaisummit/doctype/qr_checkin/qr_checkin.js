// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('QR Checkin', {
	refresh: function(frm) {
		frappe.breadcrumbs.add('Home','QR Checkin');
		// frm.call('scan_qr'
	// 	// if (frappe.is_mobile()) {
	//     // let qr_code = frm.get_field('qr_code');
	//     // frappe.barcode.scan_barcode().then(barcode => {
	// 	// 					qr_code.set_value(barcode);
	// 	// 				});
	//     // }
	// },
	// qr_code(frm){
	// 	if(frm.doc.qr_code){
	// 	frappe.call({
	// 		"method": "frappe.client.get_value",
	// 		"args": {
	// 			"doctype": "Employee",
	// 			"filters": {
	// 				"name": frm.doc.qr_code
	// 			},
	// 			"fieldname": ["employee", "employee_name","department"]
	// 		},
	// 		callback(r) {
	// 			if(r.message){
	// 			frm.set_value("employee", r.message.employee)
	// 			frm.set_value("employee_name", r.message.employee_name)
	// 			frm.set_value("department", r.message.department)
	// 			frm.set_value("qr_scan_time",frappe.datetime.now_datetime())
	// 			frm.save()
	// 		}
	// 	}
	// 	})
	// }
	}
});
