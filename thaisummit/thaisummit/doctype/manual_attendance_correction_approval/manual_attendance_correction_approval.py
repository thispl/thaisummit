# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ManualAttendanceCorrectionApproval(Document):
	def get_mp_hod(self):
		dept_list = frappe.db.get_all("User Permission",{"User":frappe.session.user,"allow":"Department"},["for_value"])
		depts = []
		for dept in dept_list:
			depts.append(dept.for_value)
		dept = str(depts).strip('[]')
		mp_list = frappe.db.sql("select * from `tabMiss Punch Application` where department in (%s) and status = 'Applied' and attendance_date between '%s' and '%s' "%(dept,self.from_date,self.to_date),as_dict=True)
		return mp_list

	def get_mp_hr(self):
		mp_list = frappe.db.sql("select * from `tabMiss Punch Application` where status = 'Approved By HOD' and attendance_date between '%s' and '%s' "%(self.from_date,self.to_date),as_dict=True)
		return mp_list
	
	def approve_miss_punch_hod(self,row,from_date,to_date):
		# frappe.errprint(type(row["in_time"]))
		doc = frappe.get_doc("Miss Punch Application",row["miss_punch_application"])
		doc.in_time = row["in_time"]
		doc.out_time = row["out_time"]
		doc.qr_scan_time = row["qr_scan_time"]
		doc.status = "Approved By HOD"
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		return 'ok'
	
	def approve_miss_punch_hr(self,row,from_date,to_date):
		doc = frappe.get_doc("Miss Punch Application",row["miss_punch_application"])
		doc.in_time = row["in_time"]
		doc.out_time = row["out_time"]
		doc.qr_scan_time = row["qr_scan_time"]
		doc.status = "Approved By HR"
		doc.save(ignore_permissions=True)
		doc.submit()
		frappe.db.commit()
		return 'ok'
