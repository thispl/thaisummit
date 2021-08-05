# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, _
from frappe.utils import formatdate

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = []
	columns += [
		_("Employee ID") + ":Data/:150",_("Employee Name") + ":Data/:200",_("Department") + ":Data/:150",_("Employee Type") + ":Data/:150",_("Shift Type") + ":Data/:100",_("Shift Date") + ":Data/:150",_("Route No") + ":Data/:100",_("Boarding Point") + ":Data/:150"
	]
	return columns

def get_data(filters):
	data = []
	if filters.department:
		shifts = frappe.db.sql("""select * from `tabShift Assignment` where start_date between '%s' and '%s' and department = '%s' and docstatus = '1' """%(filters.from_date,filters.to_date,filters.department),as_dict=True)
		for s in shifts:
			data.append([s.employee,s.employee_name,s.department,s.employee_type,s.shift_type,formatdate(s.start_date),s.route_no,s.boarding_point])
	else:
		shifts = frappe.db.sql("""select * from `tabShift Assignment` where start_date between '%s' and '%s' and docstatus = '1' """%(filters.from_date,filters.to_date),as_dict=True)
		for s in shifts:
			data.append([s.employee,s.employee_name,s.department,s.employee_type,s.shift_type,formatdate(s.start_date),s.route_no,s.boarding_point])
	return data