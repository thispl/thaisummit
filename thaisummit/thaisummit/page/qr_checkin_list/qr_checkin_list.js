frappe.pages['qr-checkin-list'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'QR Checkin List',
		single_column: true,
		card_layout:true
	});
	frappe.breadcrumbs.add('HR');
	frappe.call({
		'method': 'thaisummit.qr_utils.get_qr_list',
		callback: function (r) {
			qr_list = r.message;
			page.main.html(frappe.render_template('qr_checkin_list', {data : qr_list}));
			let employee = frappe.ui.form.make_control({
				parent: page.main.find(".employee"),
				df: {
					fieldtype: 'Data',
					fieldname: 'employee',
					placeholder: __('Enter Employee ID'),
					change: () => {
						frappe.call({
							'method': 'thaisummit.qr_utils.get_qr_list',
							'args':{
								'employee': employee.value
							},
							callback: function (r) {
								qr_list = r.message;
								page.main.html(frappe.render_template('qr_checkin_list', {data : qr_list}));
							}
						});
			}
				},
			});
			employee.refresh();
		}
	});
	
	
}