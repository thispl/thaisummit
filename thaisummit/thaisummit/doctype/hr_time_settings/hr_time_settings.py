# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime, timedelta
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr
from frappe.model.document import Document

class HRTimeSettings(Document):

	
	@frappe.whitelist()
	def payroll_date_automatic(self):
		today = getdate('2023-01-26')
		next_month = today.month + 1
		if next_month > 12:
			next_month = 1
			year = today.year + 1
		else:
			year = today.year
		next_month_25th = getdate(datetime(year, next_month, 25))
		self.payroll_start_date = today
		self.payroll_end_date = next_month_25th