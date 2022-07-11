// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pickup Plan', {
	refresh: function(frm) {
		frm.disable_save()
        frappe.breadcrumbs.add("Pickup Plan");

		$(cur_frm.fields_dict.invoice_key.input).css({ 'width': '150px', 'height': '40px', 'font-size':'18px','font-weight':'bold','background-color':'#ffedcc' })
        $(cur_frm.fields_dict.print_invoice.input).css({ 'width': '150px', 'height': '40px', 'font-size':'18px','font-weight':'bold','background-color':'#ffedcc' })
        $(cur_frm.fields_dict.invoice_detail.input).css({ 'width': '150px', 'height': '40px', 'font-size':'18px','font-weight':'bold','background-color':'#ffedcc' })
        $(cur_frm.fields_dict.invoice_status.input).css({ 'width': '150px', 'height': '40px', 'font-size':'18px','font-weight':'bold','background-color':'#ffedcc' })
        $(cur_frm.fields_dict.download.input).css({ 'width': '150px', 'height': '40px', 'font-size':'18px','font-weight':'bold','background-color':'#ffedcc' })

		frm.fields_dict.pickup_plan.$wrapper.empty().append("<h3>Pickup Plan Loading...</h3>")

		frm.call('get_pickup_plan').then(r=>{
			frm.fields_dict.pickup_plan.$wrapper.empty().append(r.message)
		})
	},
	invoice_key(frm){
		frappe.set_route('/invoice-key')
	},
	print_invoice(frm){
		frappe.set_route('Form','Print Invoice','Print Invoice')
	},
	invoice_detail(frm){
		frappe.set_route(["query-report", "Invoice Detail"]);
	},
	invoice_status(frm){
		frappe.set_route(["query-report", "Invoice Status"]);
	},
	download(frm){
		window.location.href = repl(frappe.request.url +
			'?cmd=%(cmd)s', {
			cmd: "thaisummit.thaisummit.doctype.pickup_plan.pickup_plan.download_excel",
		});
	}
});
