# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.share import add
from frappe.utils import getdate, cint, add_months, date_diff, add_days
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today

class TDSDeduction(Document):
	@frappe.whitelist()
	def get_payroll_date(self):
		date = datetime.strptime(today(), '%Y-%m-%d').date()
		if date.day > 25:
			payroll_date = add_days(get_first_day(add_months(date,-1)),25)
			frappe.errprint("HI")
			frappe.errprint(payroll_date)
			self.payroll_date = payroll_date
		else:
			frappe.errprint("HII")
			frappe.errprint(payroll_date)
			payroll_date = add_days(get_first_day(add_months(date,-2)),25)
			self.payroll_date = payroll_date

	def validate(self):
		if not frappe.db.exists('Salary Structure Assignment',{'employee':self.employee}):
			frappe.throw("No Salary Structure Found. Kindly assign a salary structure.")

	def on_submit(self):
		if self.workflow_state == 'Approved':
			adds = frappe.db.exists('Additional Salary',{'employee':self.employee,'payroll_date':self.payroll_date,'docstatus':('!=',2),'salary_component':'Tax Deducted at Source'})
			if adds:
				amt = frappe.db.get_value('Additional Salary',adds,'amount')
				frappe.db.set_value('Additional Salary',adds,'amount',self.amount + amt)
			else:
				doc = frappe.new_doc('Additional Salary')
				doc.employee = self.employee
				doc.payroll_date = self.payroll_date
				doc.salary_component = "Tax Deducted at Source"
				doc.amount = self.amount
				doc.save(ignore_permissions=True)
				doc.submit()
				frappe.db.commit()
				frappe.db.set_value('TDS Deduction',self.name,'additional_salary',doc.name)

