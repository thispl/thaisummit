# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt


import frappe
from datetime import date, timedelta
from frappe import msgprint, _
from frappe.utils import cstr, cint, getdate
from frappe.utils import cstr, add_days, date_diff, getdate
from datetime import date, timedelta, datetime


def execute(filters=None):
    columns = get_columns(filters)
    data = get_OT(filters)
    return columns,data


def get_columns(filters):
	columns = [_("Department") + ":Data/:200",]
	no_of_days = date_diff(filters.to_date,filters.from_date)
	dates = [add_days(filters.from_date,i) for i in range(0,no_of_days) ]
	
	for date in dates:		
		columns.append(_(date)+ ":Data/:150",)  	
	return columns
	
def get_OT(filters):
	data = []
	department = frappe.get_all("Department",{"is_group":"0"},)	
	for dept in department:
		no_of_days = date_diff(filters.to_date,filters.from_date)
		dates = [add_days(filters.from_date,i) for i in range(0,no_of_days)]
		count_list = [dept.name,]
		for d in dates:
			count = frappe.db.sql("""select count(`tabOvertime Request`.name) as count from `tabOvertime Request` left join `tabEmployee` on `tabOvertime Request`.employee = `tabEmployee`.name
			where `tabEmployee`.employee_type = 'WC' and `tabOvertime Request`.ot_date = '%s' and `tabOvertime Request`.department = '%s' and  `tabOvertime Request`.workflow_state = 'Approved' """%(d,dept.name),as_dict=True)
			# count = frappe.db.count("Overtime Request",{"ot_date":d,"department":dept.name,"workflow_state":'Approved','employee_type':'WC'})
			count_list.append('WC : '+ str(count[0].count))
		data.append(count_list)
	return data
	