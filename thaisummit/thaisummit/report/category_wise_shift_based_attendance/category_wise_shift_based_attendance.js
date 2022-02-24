// // Copyright (c) 2016, TEAMPRO and contributors
// // For license information, please see license.txt
// /* eslint-disable */

// frappe.query_reports["Category Wise Shift Based Attendance"] = {
// 	"filters": [
// 		{
// 			"fieldname": "from_date",
// 			"label": __("From Date"),
// 			"fieldtype": "Date",
// 			"reqd": 1,
// 			on_change: function () {
// 				var from_date = frappe.query_report.get_filter_value('from_date')
// 				frappe.call({
// 					method: "thaisummit.thaisummit.report.monthly_attendance_register.monthly_attendance_register.get_to_date",
// 					args: {
// 						from_date: from_date
// 					},
// 					callback(r) {
// 						frappe.query_report.set_filter_value('to_date', r.message);
// 						frappe.query_report.refresh();
// 					}
// 				})
// 			}
// 			}
// 		,
// 		{
// 			"fieldname": "to_date",
// 			"label": __("To Date"),
// 			"fieldtype": "Date",
// 			"reqd": 1,
// 			"default":"2021-08-30"
			
// 		},
		
// 		{
// 			"fieldname": "employee_type",
// 			"label": __("Employee Type"),
// 			"fieldtype": "Select",
// 			"reqd": 1,
// 			"options": ["WC", "BC", "FT", "NT", "CL"],
// 			"default": "WC"
// 		}
// 	],
// 	onload: function (report) {
// 		var to_date = frappe.query_report.get_filter('to_date');
// 		to_date.refresh();
// 		to_date.set_input(frappe.datetime.add_days(frappe.datetime.month_start(), 24))

// 		var from_date = frappe.query_report.get_filter('from_date');
// 		from_date.refresh();
// 		var d = frappe.datetime.add_months(frappe.datetime.month_start(), -1)
// 		from_date.set_input(frappe.datetime.add_days(d, 25))
// 	}
// }