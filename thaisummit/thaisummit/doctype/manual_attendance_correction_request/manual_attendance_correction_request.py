# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ManualAttendanceCorrectionRequest(Document):
	def get_att(self):
		# emp = frappe.db.get_value("Employee",{'user_id':frappe.session.user})
		emp = self.employee
		if emp:
			atts = frappe.db.sql("select name,employee,employee_name,department,shift,attendance_date,in_time,out_time,qr_scan_time from `tabAttendance` where employee = '%s' and attendance_date = '%s' "%(emp,self.from_date),as_dict=True)
			att_list = []
			for att in atts:
				if not frappe.db.exists("Miss Punch Application",{'attendance_date':att.attendance_date,'employee':att.employee}):
					att_list.append(att)
			return att_list
	
	def create_miss_punch_application(self,row,from_date):
		count = frappe.db.sql("select count(*) as count from `tabMiss Punch Application` where employee = '%s' and attendance_date = '%s' "%(row["employee"],from_date),as_dict=True)
		if not count[0].count >= 2:
			doc = frappe.new_doc("Miss Punch Application")
			doc.employee = row["employee"]
			doc.attendance_date = row["attendance_date"]
			doc.in_time = row["in_time"]
			doc.out_time = row["out_time"]
			doc.qr_scan_time = row["qr_scan_time"]
			doc.attendance = row["attendance"]
			doc.correction = row["correction"]
			doc.status = "Applied"
			doc.save(ignore_permissions=True)
			frappe.db.commit()
			return 'ok'
		else:
			frappe.throw("Only two Miss Punch correction is allowed in a month")