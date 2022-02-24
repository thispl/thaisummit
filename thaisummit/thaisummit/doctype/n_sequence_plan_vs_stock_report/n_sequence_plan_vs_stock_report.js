// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('N Sequence Plan vs Stock Report', {
	refresh: function(frm) {
		frm.set_value('date',frappe.datetime.nowdate())
		frm.disable_save()
		frm.call('get_html_data').then(r=>{
			frm.fields_dict.html.$wrapper.empty().append(r.message)
		})
		frm.add_custom_button(__('Download'), function () {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: "thaisummit.thaisummit.doctype.n_sequence_plan_vs_stock_report.n_sequence_plan_vs_stock_excel.download",
				args: 'date=%(date)s',
				date: frm.doc.date
			});
		});
	},
	date(frm){
		frm.call('get_html_data').then(r=>{
			frm.fields_dict.html.$wrapper.empty().append(r.message)
		})
	}
});
