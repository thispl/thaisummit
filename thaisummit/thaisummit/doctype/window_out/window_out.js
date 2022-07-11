// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Window OUT', {
	refresh: function (frm) {
		frm.disable_save()
		frappe.breadcrumbs.add("Window OUT");
		$(cur_frm.fields_dict.record_out_data.input).css({ 'width': '150px', 'height': '40px', 'font-size': '15px', 'font-weight': 'bold', 'background-color': '#ffedcc' })
		$('*[data-fieldname="window_out"]').find('.grid-remove-rows').hide();
		$('*[data-fieldname="window_out"]').find('.grid-remove-all-rows').hide();
		$('*[data-fieldname="window_out"]').find('.grid-add-row').remove()
		frm.call('get_invoices')
			.then(r => {
				$.each(r.message, function (i, d) {
					frm.add_child('window_out', {
						'supplier_name': d[0],
						'invoice_no': d[1],
						'std_out_time': d[2],
						'in_time': d[3],
						'planned_out_time': d[4]
					})
				})
				frm.refresh_field('window_out')
			})
	},
	record_out_data(frm) {
		if (frm.doc.vehicle_no) {
			$.each(frm.doc.window_out, function (i, d) {
				if (d.__checked == 1) {
					if (!d.out_bin){
						frappe.throw('Please Enter No of Bins')
					}
				}})
			$.each(frm.doc.window_out, function (i, v) {
				if (v.__checked == 1) {
					frm.call('record_out_data', {
						row: v,
					})
						.then(r => {
							console.log(r.message)
							if (r.message == 'OK') {
								frappe.msgprint("Recorded Successfully")
								frm.reload_doc();
							}
						})
				}
			})
		}
		else{
			frappe.msgprint('Please Enter Vehicle No.')
		}
	}
});

// frappe.ui.form.on('Window OUT Child', {
// 	actual_out_time(frm, cdt, cdn) {
// 		var child = locals[cdt][cdn]
// 		if (child.actual_out_time) {
// 			frm.call('get_delay', {
// 				child: child
// 			})
// 				.then(r => {
// 					if (r.message) {
// 						child.duration = r.message;
// 						child.delaymins = r.message - child.std_out_time
// 						frm.refresh_field('window_out')
// 					}
// 				})
// 		}
// 	}
// })