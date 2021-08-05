// Copyright (c) 2016, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */


frappe.query_reports["Monthly Overtime Person Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1 ,
			"default": "2021-04-23",
			on_change: function() {
				var from_date = frappe.query_report.get_filter_value('from_date')
				frappe.call({
					method: "thaisummit.thaisummit.report.monthly_attendance_register.monthly_attendance_register.get_to_date",
					args:{
						from_date: from_date
					},
					callback(r){
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
			"reqd": 1 ,
			"read_only": 1
		},
	
	],

	onload: function(report) {	
		var to_date = frappe.query_report.get_filter('to_date');
		to_date.refresh();
		to_date.set_input(frappe.datetime.add_days(frappe.datetime.month_start(),24))
		// var from_date = frappe.query_report.get_filter('from_date');
		// from_date.refresh();
		// var d = frappe.datetime.add_months(frappe.datetime.month_start(),-1)
		// from_date.set_input(frappe.datetime.add_days(d,25))
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
