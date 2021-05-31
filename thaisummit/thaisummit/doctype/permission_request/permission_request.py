# -*- coding: utf-8 -*-
# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime,timedelta,date,time
from frappe.utils import get_first_day, get_last_day

class PermissionRequest(Document):
	def get_endtime1(Self,start_time):
		time = datetime.strptime(start_time, "%H:%M:%S")
		end_time = timedelta(hours=2) + time
		return str(end_time.time())

	def get_endtime2(Self,end_time):
		time = datetime.strptime(end_time, "%H:%M:%S")
		start_time = time - timedelta(hours=2)
		return str(start_time.time())
	
	# def submit_doc(self):
	# 	self.status = "Approved"
	# 	self.submit()
	# 	frappe.db.commit()
	# 	return "ok"

	def validate(self):
		self.hours = '2'
		month_start = get_first_day(self.attendance_date)
		month_end = get_last_day(self.attendance_date)
		count = frappe.db.sql("select count(*) as count from `tabPermission Request` where employee = '%s' and attendance_date between '%s' and '%s' and name != '%s' and workflow_state != 'Rejected' and docstatus != '2' "%(self.employee,month_start,month_end,self.name),as_dict=True)
		frappe.errprint(count)
		if count[0].count >= 2:
			frappe.throw("Only 2 permissions are allowed for a month")