frappe.query_reports["TAG Master Report Based on Time"] = {
	"filters": [
		{
			"fieldname":"from_time",
			"label": __("From Time"),
			"fieldtype": "Time",
			// "reqd": 1,
			"default": frappe.datetime.now_time()
		},
		{
			"fieldname":"to_time",
			"label": __("To Time"),
			"fieldtype": "Time",
			// "reqd": 1,
			"default": frappe.datetime.now_time()
		}
    ]
}