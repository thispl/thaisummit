frappe.pages['pickup-plan'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Pickup Plan',
		single_column: true
	});
	frappe.breadcrumbs.add("Pickup Plan");
	window.location.href = "/pickup_plan";
}