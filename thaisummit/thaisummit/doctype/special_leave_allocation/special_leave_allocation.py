# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SpecialLeaveAllocation(Document):
	def update_leave_allocation(self,allocation):
		# update_allocation = frappe.get_all("Leave Allocation",{'employee' :self.employee_id},['leave_type','new_leaves_allocated'])
		# for u in update_allocation:
		# 	la =frappe.db.sql("""select employee from `tabLeave Allocation` where  leave_type = '%s'  order by name""" %(row["parts_no"],row["quantity"]),as_dict=True)[0]

