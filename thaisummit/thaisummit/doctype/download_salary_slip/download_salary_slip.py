# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from calendar import month
import frappe
from frappe.model.document import Document
from frappe.monitor import start

class DownloadSalarySlip(Document):
	@frappe.whitelist()
	def get_salary_slip(self):
		if self.month == 'Jan':
			start_date = str((int(self.year) - 1)) + '-12-26'
		else:
			start_date = self.year + '-' + str(month.get(self.month)-1) + '-26'
		slips = frappe.db.sql("""select name from `tabSalary Slip` where start_date = '%s' and employee = '%s' and docstatus = 1 """%(start_date,self.employee),as_dict=True)
		return slips


month = {
	'Jan':1,
	'Feb':2,
	'Mar':3,
	'Apr':4,
	'May':5,
	'Jun':6,
	'Jul':7,
	'Aug':8,
	'Sep':9,
	'Oct':10,
	'Nov':11,
	'Dec':12
}