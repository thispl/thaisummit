frappe.pages['food-scan-entry'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Food Scan Entry',
		single_column: true
	});
	frappe.breadcrumbs.add('Canteen');

	page.add_field({
		fieldname: 'party_id',
		label: __('Employee/Guest ID'),
		fieldtype: 'Data',
		reqd: 1,
		change: function() {
			frappe.call({
				'method': 'thaisummit.qr_utils.get_canteen_user_details',
				args: {
					user: this.get_value(),
				},
				callback: function (r) {
					console.log(r.message)
					party_details = r.message;
					// page.main.html(frappe.render_template('food_scan_entry', {data : party_details}));
				}
			});
		}
	});
	// employee/guest_id(frm)
	// {
	//     if(frm.doc.employee/guest_id)
	//     {
	//         var id_number = frm.doc.employee/guest_id;
	//         var change_upper_case = id_number.toUpperCase();
	//         frm.set_value('employee/guest_id',change_upper_case);
	//     }
	// }
	// onload(frm) 
	// {
	// 	var time = new Date().toLocaleTimeString();
	// 	var time_format = moment(time, "h:mm:ss A").format("HH:mm");
	// 	frm.set_value('time', time_format)
	// }
}