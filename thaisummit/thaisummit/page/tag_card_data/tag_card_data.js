frappe.pages['tag-card-data'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Tag Card Details',
		single_column: true
	});
	let emp_details = {};
	frappe.call({
		'method': 'thaisummit.www.qr_checkin.get_tag_card',
		args: {
			tag_card_no : result
		},
		callback: function (r) {
			tag_card_details = r.message[1];
			console.log(r.message)
			page.main.html(frappe.render_template('tag_card_data', {data : tag_card_details}));
		}
	});
}