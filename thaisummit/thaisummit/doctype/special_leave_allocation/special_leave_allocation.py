# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SpecialLeaveAllocation(Document):
	def update_leave_allocation(self,allocation):
		lle = frappe.db.sql("select name from `tabLeave Ledger Entry` where employee = %s and '%s' between from_date and to_date and leave_type = 'Earned Leave' "%(self.employee_id,self.date),as_dict=True)
		frappe.db.set_value('Leave Ledger Entry',lle[0].name,'leaves','2')
		# for u in update_allocation:
		# 	la =frappe.db.sql("""select employee from `tabLeave Allocation` where  leave_type = '%s'  order by name""" %(row["parts_no"],row["quantity"]),as_dict=True)[0]

