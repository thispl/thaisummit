frappe.pages['qr-checkin-list'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'QR Checkin List',
		single_column: true,
		card_layout:true
	});
	frappe.breadcrumbs.add('HR');
	let emp_details = {};
	frappe.call({
		'method': 'thaisummit.qr_utils.get_qr_list',
		callback: function (r) {
			qr_list = r.message;
			page.main.html(frappe.render_template('qr_checkin_list', {data : qr_list}));
		}
	});
}