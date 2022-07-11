// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Window IN', {
	refresh: function (frm) {
		frm.disable_save()
		frappe.breadcrumbs.add("Window IN");
		$(cur_frm.fields_dict.record_in_data.input).css({ 'width': '150px', 'height': '40px', 'font-size': '15px', 'font-weight': 'bold', 'background-color': '#ffedcc' })
		$('*[data-fieldname="window_in"]').find('.grid-remove-rows').hide();
		$('*[data-fieldname="window_in"]').find('.grid-remove-all-rows').hide();
		$('*[data-fieldname="window_in"]').find('.grid-add-row').remove()
		frm.trigger('date')
	},
	supplier(frm){
		frm.trigger('date')
	},
	date(frm){
		if (frm.doc.date){
			frm.call('get_invoices')
			.then(r => {
				frm.clear_table('window_in')
				$.each(r.message, function (i, d) {
					frm.add_child('window_in', {
						'supplier_name': d[0],
						'date': d[1],
						'invoice_no': d[2],
						'no_of_bins': d[3],
						'amount': d[4],
						'std_in_time': d[5]
					})
				})
				frm.refresh_field('window_in')
			})
		}
	},
	record_in_data(frm) {
		$.each(frm.doc.window_in, function (i, v) {
			if (v.__checked == 1) {
				frm.call('record_in_data', {
					row: v
				})
					.then(r => {
						if (r.message == 'OK') {
							frappe.msgprint("Recorded Successfully")
							frm.reload_doc();
						}
					})
			}
		})
	}
});

frappe.ui.form.on('Window IN Child', {
	actual_in_time(frm, cdt, cdn) {
		var child = locals[cdt][cdn]
		if (child.actual_in_time) {
			frm.call('get_delay', {
				child: child
			})
				.then(r => {
					if (r.message) {
						child.delaymins = r.message;
						frm.refresh_field('window_in')
					}
				})
		}
	}
})