// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cancel Invoice', {
	refresh: function (frm) {
        frappe.breadcrumbs.add("Cancel Invoice");
		frm.disable_save()
		$('*[data-fieldname="cancel_invoice_child"]').find('.grid-remove-rows').hide();
		$('*[data-fieldname="cancel_invoice_child"]').find('.grid-remove-all-rows').hide();
		$('*[data-fieldname="cancel_invoice_child"]').find('.grid-add-row').remove()
	},
	cancel(frm) {
		$.each(frm.doc.cancel_invoice_child, function (i, v) {
			if (v.__checked == 1) {
				frappe.db.set_value("TSAI Invoice", v.invoice_no, 'status', "CANCELLED")
				frappe.msgprint("Sucessfully Cancellled Invoice - "+ v.invoice_no)
			}
		})
		frm.reload_doc()
	},
	supplier(frm) {
		frm.trigger('get_invoice')
	},
	from_date(frm) {
		frm.trigger('get_invoice')
	},
	to_date(frm) {
		frm.trigger('get_invoice')
	},
	get_invoice(frm) {
		if (frm.doc.supplier) {
			if (frm.doc.from_date && frm.doc.to_date) {
				frappe.call({
					method: 'frappe.client.get_list',
					args: {
						doctype: 'TSAI Invoice',
						filters: {
							'status': 'OPEN',
							'supplier_code': frm.doc.supplier,
							'invoice_date': ['between', [frm.doc.from_date, frm.doc.to_date]]
						},
						fields: ['name', 'invoice_date']
					},
					callback(r) {
						frm.clear_table('cancel_invoice_child')
						$.each(r.message, function (i, d) {
							frm.add_child('cancel_invoice_child', {
								'invoice_no': d.name,
								'invoice_date': d.invoice_date
							})
						})
						frm.refresh_field('cancel_invoice_child')
					}
				})
			}
			else {
				frm.set_value('cancel_invoice_child', [])
			}
		}
		else {
			frm.set_value('cancel_invoice_child', [])
		}
	}
});
