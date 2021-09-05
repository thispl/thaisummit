frappe.query_reports["Monthly Attendance Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_start(),
			"reqd": 1
		},
        {
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_end(),
			"reqd": 1
		},
        {
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
            "option": "Employee",
			"reqd": 1,
		}
    ],
    "onload": function() {
		return  frappe.call({
			"method": "frappe.client.get_value",
			"args": {
				"doctype": "Employee",
				"filters": {
					"user_id": frappe.session.user
				},
				"fieldname": ["employee"]
			},
			callback: function(r) {
                console.log(r.message)
				var emp_filter = frappe.query_report.get_filter('employee');
				emp_filter.df.default = r.message.employee
				emp_filter.refresh();
				emp_filter.set_input(emp_filter.df.default);
			}
		});
	},
    onload_post_render(report){
        report.page.add_inner_button(__('Apply Miss Punch Request'), function() {
            frappe.set_route(["Form","Manual Attendance Correction Request"]);
        });
    }
}