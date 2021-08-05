// Copyright (c) 2016, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Shift Assignment Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.now_date()
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.now_date()
		},
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department"
		}
	],

	// onload: function (report) {
	// 	var to_date = frappe.query_report.get_filter('to_date');
	// 	to_date.refresh();
	// 	to_date.set_input(frappe.datetime.add_days(frappe.datetime.month_start(), 24))

	// 	var from_date = frappe.query_report.get_filter('from_date');
	// 	from_date.refresh();
	// 	var d = frappe.datetime.add_months(frappe.datetime.month_start(), -1)
	// 	from_date.set_input(frappe.datetime.add_days(d, 25))

	// 	var employee = frappe.query_report.get_filter('employee');
	// 	employee.refresh();
	// 	var employee_type = frappe.query_report.get_filter('employee_type');
	// 	employee_type.refresh();
	// 	if (frappe.session.user != "Administrator") {
	// 		frappe.db.get_value("Employee", { 'user_id': frappe.session.user }, ["name", "employee_type"], (r) => {
	// 			employee.set_input(r.name)
	// 			employee_type.set_input(r.employee_type)
	// 			report.refresh()
	// 		})
	// 	}
	// },
};
