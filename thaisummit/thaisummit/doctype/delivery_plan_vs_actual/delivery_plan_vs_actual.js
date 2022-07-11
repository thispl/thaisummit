// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Delivery Plan vs Actual', {
	refresh: function (frm) {
		frm.disable_save()
		frm.set_value('from_date', frappe.datetime.add_days(frappe.datetime.nowdate(), -1))
		frm.set_value('to_date', frappe.datetime.nowdate())
	},
	view(frm) {
		if (frm.doc.from_date && frm.doc.to_date) {
			frm.trigger('display_data')
		}
	},
	display_data(frm) {
		frappe.call({
			method: "thaisummit.thaisummit.doctype.delivery_plan_vs_actual.delivery_plan_vs_actual.get_data",
			args: {
				from_date: frm.doc.from_date,
				to_date: frm.doc.to_date
			},
			freeze: true,
			callback(r) {
				if (r.message) {
					frm.fields_dict.html.$wrapper.empty().append(r.message)
				}
			}
		})
	},
	download: function (frm) {
		if (frm.doc.from_date && frm.doc.to_date) {
			// window.location.href = repl(frappe.request.url +
			// 	'?cmd=%(cmd)s&%(args)s', {
			// 	cmd: "thaisummit.thaisummit.doctype.delivery_plan_vs_actual.delivery_plan_vs_actual.download",
			// 	args: 'from_date=%(from_date)s&to_date=%(to_date)s',
			// 	from_date: frm.doc.from_date,
			// 	to_date: frm.doc.to_date,
			// });
			frappe.call({
				method: "thaisummit.thaisummit.doctype.delivery_plan_vs_actual.delivery_plan_vs_actual.enqueue_download",
				args: {
					from_date: frm.doc.from_date,
					to_date: frm.doc.to_date,
				}
			})
		} else {
			frappe.throw('Please Enter From Date and To Date')
		}
	},
});
