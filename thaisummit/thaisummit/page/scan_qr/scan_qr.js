frappe.pages['scan-qr'].on_page_load = function (wrapper) {
	let me = this;
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Scan QR',
		single_column: true,
		card_layout : true
	});
	frappe.breadcrumbs.add('HR');
	
	let emp_details = {};
	frappe.call({
		'method': 'thaisummit.qr_utils.get_qr_details',
		args: {
			user: frappe.session.user
		},
		callback: function (r) {
			qr_details = r.message;
			page.main.html(frappe.render_template('scan_qr', {data : qr_details}));
		}
	});
	
	
	// window.location.href = "/qr_checkin";
}



let show_employee_info = function (me) {
	frappe.call({
		'method': 'frappe.client.get_value',
		args: {
			doctype: "Employee",
			filters: { "user_id": frappe.session.user },
			fieldname: ["employee_name", "department"]
		},
		callback: function (r) {
			emp_details = r.message;
			
		}
	});
};



