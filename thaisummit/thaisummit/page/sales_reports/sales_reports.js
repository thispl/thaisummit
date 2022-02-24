frappe.pages['sales-reports'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'None',
		single_column: true
	});
	frappe.breadcrumbs.add('HR');
	let report_type = frappe.ui.form.make_control({
		parent: page.main.find(".report_type"),
		df: {
			fieldtype: 'Select',
			options:['Daily Sales Report', 'Daily Sales Report Summary'].join('\n'),
			fieldname: 'report_type',
			placeholder: __('Select Report'),
			change: () => {
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s&%(args)s', {
					cmd: path,
					args: args,
					from_date : frm.doc.from_date,
					to_date : frm.doc.to_date,
				});
	}
		},
	});
}