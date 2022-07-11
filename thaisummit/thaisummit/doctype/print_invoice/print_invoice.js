// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Print Invoice', {
	refresh: function (frm) {
		frm.disable_save();
        frappe.breadcrumbs.add("Print Invoice");
		$('*[data-fieldname="print_invoice_child"]').find('.grid-remove-rows').hide();
		$('*[data-fieldname="print_invoice_child"]').find('.grid-remove-all-rows').hide();
		$('*[data-fieldname="print_invoice_child"]').find('.grid-add-row').remove()

		frm.set_value("from_date", frappe.datetime.add_days(frappe.datetime.nowdate(),-6));
		frm.set_value("to_date", frappe.datetime.nowdate());

		frm.fields_dict["print_invoice_child"].grid.add_custom_button(__('Download TAG Card'),
			function () {
				$.each(frm.doc.print_invoice_child, function (i, d) {
					if (d.__checked == 1) {
						window.open(
							frappe.urllib.get_full_url(`/api/method/frappe.utils.print_format.download_pdf?
								doctype=${encodeURIComponent("TSAI Invoice")}
								&name=${encodeURIComponent(d.invoice_no)}
								&format=${encodeURIComponent('TSAI Tag Card')}`)
						);
						window.open(
							frappe.urllib.get_full_url(`/api/method/frappe.utils.print_format.download_pdf?
								doctype=${encodeURIComponent("TSAI Invoice")}
								&name=${encodeURIComponent(d.invoice_no)}
								&format=${encodeURIComponent('TSAI Invoice')}`)
						);
					}
				})
			}
		).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })

		frm.fields_dict["print_invoice_child"].grid.add_custom_button(__('Download Invoice'),
			function () {
				$.each(frm.doc.print_invoice_child, function (i, d) {
					if (d.__checked == 1) {
						window.open(
							frappe.urllib.get_full_url(`/api/method/frappe.utils.print_format.download_pdf?
								doctype=${encodeURIComponent("TSAI Invoice")}
								&name=${encodeURIComponent(d.invoice_no)}
								&format=${encodeURIComponent('TSAI Invoice')}`)
						);
					}
				})
			}
		).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })


	},
	from_date(frm) {
		if (frm.doc.from_date && frm.doc.to_date) {
			frm.trigger('get_invoice')
		}
	},
	to_date(frm) {
		if (frm.doc.from_date && frm.doc.to_date) {
			frm.trigger('get_invoice')
		}
	},
	supplier(frm) {
		if (frm.doc.from_date && frm.doc.to_date && frm.doc.supplier) {
			frm.trigger('get_invoice')
		}
	},
	get_invoice(frm) {
		frappe.call({
			method: "thaisummit.thaisummit.doctype.print_invoice.print_invoice.get_supplier_invoice",
			args: {
				from_date : frm.doc.from_date,
				to_date : frm.doc.to_date,
				supplier : frm.doc.supplier
			},
			callback(r) {
				frm.clear_table('print_invoice_child')
				$.each(r.message, function (i, d) {
					frm.add_child('print_invoice_child', {
						invoice_no: d.name,
						invoice_date: d.invoice_date,
						supplier_name : d.supplier_name
					})
					frm.refresh_field('print_invoice_child')
				})
			}
		})
	},
});
