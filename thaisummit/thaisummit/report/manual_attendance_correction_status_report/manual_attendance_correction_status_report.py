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
		_("Employee ID") + ":Data/:150",_("Employee Name") + ":Data/:200",_("Department") + ":Data/:150",_("Attendance Date") + ":Data/:150",_("Staus") + ":Data/:150",_("IN Time") + ":Datetime/:150",_("OUT Time") + ":Datetime/:150",_("QR Shift") + ":Data/:100",_("Corrected") + ":Data/:200"
	]
	return columns

def get_data(filters):
	data = []
	conditions = ''
	if filters.employee:
		conditions += "and employee = '%s' "%(filters.employee)
	if filters.status:
		conditions += "and workflow_state = '%s' "%(filters.status)
	roles = frappe.get_roles(frappe.session.user)
	if 'System Manager' in roles:
		mps = frappe.db.sql("""select * from `tabMiss Punch Application` where attendance_date between '%s' and '%s' %s """%(filters.from_date,filters.to_date,conditions),as_dict=True)
		for s in mps:
			correction = ''
			frappe.errprint(s.in_time)
			frappe.errprint(frappe.db.get_value('Employee Checkin',{'time':s.in_time,'employee':s.employee},'time'))
			if not frappe.db.exists('Employee Checkin',{'time':s.in_time,'employee':s.employee}):
				correction += 'IN Time '
			if not frappe.db.exists('Employee Checkin',{'time':s.out_time,'employee':s.employee}):
				correction += 'OUT Time '
			emp_type = frappe.db.get_value('Employee',s.employee,'employee_type')
			if emp_type != 'WC':
				if not frappe.db.exists('QR Checkin',{'employee':s.employee,'qr_shift':s.qr_shift}):
					correction += 'QR Scan'
			data.append([s.employee,s.employee_name,s.department,s.workflow_state,formatdate(s.attendance_date),s.in_time,s.out_time,s.qr_shift,correction])
	else:
		if filters.employee:
			mps = frappe.db.sql("""select * from `tabMiss Punch Application` where attendance_date between '%s' and '%s' %s """%(filters.from_date,filters.to_date,conditions),as_dict=True)
			for s in mps:
				correction = ''
				if not frappe.db.exists('Employee Checkin',{'time':s.in_time,'employee':s.employee}):
					correction += 'IN Time '
				if not frappe.db.exists('Employee Checkin',{'time':s.out_time,'employee':s.employee}):
					correction += 'OUT Time '
				emp_type = frappe.db.get_value('Employee',s.employee,'employee_type')
				if emp_type != 'WC':
					if not frappe.db.exists('QR Checkin',{'employee':s.employee,'qr_shift':s.qr_shift}):
						correction += 'QR Scan'
				data.append([s.employee,s.employee_name,s.department,s.workflow_state,formatdate(s.attendance_date),s.in_time,s.out_time,s.qr_shift,correction])
		# else:
		# 	frappe.msgprint('Kindly Enter your Employee ID')
	return data