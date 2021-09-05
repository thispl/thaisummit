frappe.pages['tag-monitoring'].on_page_load = (wrapper) => {
	let page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __('TAG Monitor'),
		single_column: true
	});

	frappe.breadcrumbs.add("Tag Monitor");
	window.location.href = "/tag_monitoring_tool";
	// window.open('https://thaisummit.teamproit.com/tag_monitoring_tool', '_blank');


};
