# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today

class EmployeeWelfare(Document):
	pass

@frappe.whitelist()
def create_employee_welfare(employee):
	welfare_occasion = frappe.db.get_value('Employee Welfare Scan',None,'welfare_occasion')
	welfare_item = frappe.db.get_value('Employee Welfare Scan',None,'welfare_item')
	if not frappe.db.exists('Employee',{'name':employee,'status':'Active'}):
		return 'Employee Not Found'
	elif frappe.db.exists('Employee Welfare',{'employee':employee,'welfare_occasion':welfare_occasion,'welfare_item':welfare_item}):
		return 'Already Scanned'
	else:
		ew = frappe.new_doc('Employee Welfare')
		ew.employee = employee
		ew.date = today()
		ew.welfare_item = welfare_item
		ew.welfare_occasion = welfare_occasion
		ew.save(ignore_permissions=True)
		frappe.db.commit()
		return 'Successfully Scanned'
	
	
