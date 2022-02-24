frappe.pages['invoice-key'].on_page_load = (wrapper) => {
	let page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __('Invoice Key'),
		single_column: true
	});

	frappe.breadcrumbs.add("Invoice Key");
	window.location.href = "/invoice_key";
	// window.open('https://thaisummit.teamproit.com/tag_monitoring_tool', '_blank');


};
