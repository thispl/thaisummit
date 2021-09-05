frappe.query_reports["IYM Card IN & OUT Overall Report"] = {
	"filters": [
		{
			"fieldname":"from_datetime",
			"label": __("From Datetime"),
			"fieldtype": "Datetime",
			"default": frappe.datetime.now_datetime()
		},
		{
			"fieldname":"to_datetime",
			"label": __("To Datetime"),
			"fieldtype": "Datetime",
			"default": frappe.datetime.now_datetime()
		}
    ]
}