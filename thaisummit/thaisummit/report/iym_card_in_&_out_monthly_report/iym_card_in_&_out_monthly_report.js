frappe.query_reports["IYM Card IN & OUT Monthly Report"] = {
 
	"filters": [
		{
			"fieldname":"monthly",
			"label": __("Monthly"),
            "fieldtype": "Select",
            // "reqd": 1,
            "default": new Date().toLocaleString('default', { month: 'long' }),
            "options":["Januvary",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"]
		},
		
    ]
}