// Copyright (c) 2016, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Manual Attendance Correction Status Report"] = {
	"filters": [
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			// "read_only": 1,
			// "reqd": 1
		},
		{
			"fieldname": "from_date",
			"label": __("Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": ["","Pending for HOD","Approved","Pending for HR GM"]
		},
		
	],
	onload: function (report) {
		var to_date = frappe.query_report.get_filter('to_date');
		to_date.refresh();
		to_date.set_input(frappe.datetime.add_days(frappe.datetime.month_start(), 24))

		var from_date = frappe.query_report.get_filter('from_date');
		from_date.refresh();
		var d = frappe.datetime.add_months(frappe.datetime.month_start(), -1)
		from_date.set_input(frappe.datetime.add_days(d, 25))

		var employee = frappe.query_report.get_filter('employee');
		employee.refresh();
		if (!frappe.user.has_role("System Manager")) {
			frappe.db.get_value("Employee", { 'user_id': frappe.session.user }, ["name", "employee_type"], (r) => {
				employee.set_input(r.name)
				report.refresh()
			})
		}
	},
};
