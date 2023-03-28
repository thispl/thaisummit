frappe.pages['tag-card-details'].on_page_load = function(wrapper) {
	let me = this;
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Scan Tag Card',
		single_column: true,
		card_layout : true
	});
	frappe.breadcrumbs.add('HR');
	
	let emp_details = {};
	frappe.call({
		'method': 'thaisummit.qr_utils.get_qr_details_tag_card',
		args: {
			user: frappe.session.user
		},
		callback: function (r) {
			qr_details = r.message;
			console.log(r.message)
			page.main.html(frappe.render_template('tag_card_details', {data : qr_details}));
		}
	});
}