# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
import json

class ManualAttendanceCorrectionRequest(Document):
	@frappe.whitelist()
	def get_att(self):
		# emp = frappe.db.get_value("Employee",{'user_id':frappe.session.user})
		emp = self.employee
		if emp:
			atts = frappe.db.sql("select name,employee,employee_name,department,shift,attendance_date,in_time,out_time,qr_shift from `tabAttendance` where employee = '%s' and attendance_date = '%s' "%(emp,self.from_date),as_dict=True)
			att_list = []
			for att in atts:
				if not frappe.db.exists("Miss Punch Application",{'attendance_date':att.attendance_date,'employee':att.employee}):
					att_list.append(att)
			return att_list
	
	# @frappe.whitelist()
	# def create_miss_punch_application(self,row,from_date):
	# 	date = datetime.strptime(from_date, '%Y-%m-%d').date()
	# 	last_month = add_months(date,-1)
	# 	last_month_start = get_first_day(last_month)
	# 	allowed_from = add_days(last_month_start,25)
	# 	cur_month_start = get_first_day(date)
	# 	allowed_till = add_days(cur_month_start,24)
	# 	count = frappe.db.sql("select count(*) as count from `tabMiss Punch Application` where employee = '%s' and attendance_date between '%s' and '%s' "%(row["employee"],allowed_from,allowed_till),as_dict=True)
	# 	if not count[0].count >= 2:
	# 		doc = frappe.new_doc("Miss Punch Application")
	# 		doc.employee = row["employee"]
	# 		doc.attendance_date = row["attendance_date"]
	# 		doc.in_time = row["in_time"]
	# 		doc.out_time = row["out_time"]
	# 		doc.qr_shift = row["qr_shift"]
	# 		doc.attendance = row["attendance"]
	# 		doc.correction = row["correction"]
	# 		doc.save(ignore_permissions=True)
	# 		frappe.db.commit()
	# 		self.mp_child = ''
	# 		self.employee = ''
	# 		self.employee_name = ''
	# 		self.from_date = ''
	# 		return 'ok'
	# 	else:
			# frappe.throw("Only two Miss Punch correction is allowed in a month")

@frappe.whitelist()
def create_miss_punch(row,from_date):
	row = json.loads(row)
	date = datetime.strptime(from_date, '%Y-%m-%d').date()
	last_month = add_months(date,-1)
	last_month_start = get_first_day(last_month)
	allowed_from = add_days(last_month_start,25)
	cur_month_start = get_first_day(date)
	allowed_till = add_days(cur_month_start,24)
	count = frappe.db.sql("select count(*) as count from `tabMiss Punch Application` where employee = '%s' and attendance_date between '%s' and '%s' "%(row["employee"],allowed_from,allowed_till),as_dict=True)
	if not count[0].count >= 2:
		doc = frappe.new_doc("Miss Punch Application")
		doc.employee = row["employee"]
		doc.attendance_date = row["attendance_date"]
		doc.in_time = row["in_time"]
		doc.out_time = row["out_time"]
		doc.qr_shift = row["qr_shift"]
		doc.attendance = row["attendance"]
		doc.correction = row["correction"]
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		return 'ok'
	else:
		frappe.throw("Only two Miss Punch correction is allowed in a month")