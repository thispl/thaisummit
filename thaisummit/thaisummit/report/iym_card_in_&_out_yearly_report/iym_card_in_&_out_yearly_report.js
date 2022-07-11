frappe.query_reports["IYM Card IN & OUT Yearly Report"] = {
 
	"filters": [
		{
			"fieldname":"yearly",
			"label": __("Yearly"),
            "fieldtype": "Select",
            "default":"2022",
            "options":[
            "2021",
            "2022",
            "2023",
            "2024",
            "2025"
            ]
		},
		
    ]
}