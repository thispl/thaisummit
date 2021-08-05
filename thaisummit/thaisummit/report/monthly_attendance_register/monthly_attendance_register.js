// Copyright (c) 2016, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly Attendance Register"] = {
	"filters": [
		// {
		// 	"fieldname": "month",
		// 	"label": __("Month"),
		// 	"fieldtype": "Select",
		// 	"reqd": 1 ,
		// 	"options": [
		// 		{ "value": 1, "label": __("Jan") },
		// 		{ "value": 2, "label": __("Feb") },
		// 		{ "value": 3, "label": __("Mar") },
		// 		{ "value": 4, "label": __("Apr") },
		// 		{ "value": 5, "label": __("May") },
		// 		{ "value": 6, "label": __("June") },
		// 		{ "value": 7, "label": __("July") },
		// 		{ "value": 8, "label": __("Aug") },
		// 		{ "value": 9, "label": __("Sep") },
		// 		{ "value": 10, "label": __("Oct") },
		// 		{ "value": 11, "label": __("Nov") },
		// 		{ "value": 12, "label": __("Dec") },
		// 	],
		// 	"default": frappe.datetime.str_to_obj(frappe.datetime.get_today()).getMonth() + 1,
		// 	// on_change: function() {
		// 	// 		frappe.query_report.set_filter_value('to_date', );
		// 	// }
		// },
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			on_change: function () {
				var from_date = frappe.query_report.get_filter_value('from_date')
				frappe.call({
					method: "thaisummit.thaisummit.report.monthly_attendance_register.monthly_attendance_register.get_to_date",
					args: {
						from_date: from_date
					},
					callback(r) {
						frappe.query_report.set_filter_value('to_date', r.message);
						frappe.query_report.refresh();
					}
				})
			}
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"read_only": 1
		},
		{
			"fieldname": "employee_type",
			"label": __("Employee Type"),
			"fieldtype": "Select",
			"reqd": 1,
			"options": ["WC", "BC", "FT", "NT", "CL"],
			// "default": "WC"
		},
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department"
		},
		{
			"fieldname": "year",
			"label": __("Year"),
			"fieldtype": "Select",
			"reqd": 0,
			"hidden": 1
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			get_query: () => {
				var company = frappe.query_report.get_filter_value('company');
				return {
					filters: {
						'company': company
					}
				};
			}
		},
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1,
			"hidden": 1
		},
		{
			"fieldname": "group_by",
			"label": __("Group By"),
			"fieldtype": "Select",
			"options": ["", "Branch", "Grade", "Department", "Designation"]
		},
		// {
		// 	"fieldname":"summarized_view",
		// 	"label": __("Summarized View"),
		// 	"fieldtype": "Check",
		// 	"Default": 0,
		// }
	],

	"onload": function () {
		return frappe.call({
			method: "erpnext.hr.report.monthly_attendance_sheet.monthly_attendance_sheet.get_attendance_years",
			callback: function (r) {
				var year_filter = frappe.query_report.get_filter('year');
				year_filter.df.options = r.message;
				year_filter.df.default = r.message.split("\n")[0];
				year_filter.refresh();
				year_filter.set_input(year_filter.df.default);
			}
		});
	},
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
		var employee_type = frappe.query_report.get_filter('employee_type');
		employee_type.refresh();
		if (frappe.session.user != "Administrator") {
			frappe.db.get_value("Employee", { 'user_id': frappe.session.user }, ["name", "employee_type"], (r) => {
				employee.set_input(r.name)
				employee_type.set_input(r.employee_type)
				report.refresh()
			})
		}
	},
	// from_date: function(report){
	// 	console.log('hi')
	// 	var filters = report.get_values();
	// 	var to_date = frappe.query_report.get_filter('to_date');
	// 	to_date.refresh();
	// 	// to_date.set_input(frappe.datetime.add_days(filters.from_date,30))
	// 	to_date.set_input(filters.from_date)
	// }
};
