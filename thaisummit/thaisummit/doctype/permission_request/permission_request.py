# -*- coding: utf-8 -*-
# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime,timedelta,date,time
from frappe.utils import get_first_day, get_last_day, format_datetime,get_url_to_form
from frappe import msgprint

class PermissionRequest(Document):
	@frappe.whitelist()
	def get_endtime1(Self,start_time):
		time = datetime.strptime(start_time, "%H:%M:%S")
		end_time = timedelta(hours=2) + time
		return str(end_time.time())

	@frappe.whitelist()
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
		today = frappe.db.sql("select count(*) as count from `tabPermission Request` where employee = '%s' and attendance_date = '%s' and name != '%s' and workflow_state != 'Rejected' "%(self.employee,self.attendance_date,self.name),as_dict=True)
		if today[0].count >= 1:
			frappe.throw("Only 1 permission are allowed for a day")
		count = frappe.db.sql("select count(*) as count from `tabPermission Request` where employee = '%s' and attendance_date between '%s' and '%s' and name != '%s' and workflow_state != 'Rejected' "%(self.employee,month_start,month_end,self.name),as_dict=True)
		if count[0].count >= 2:
			frappe.throw("Only 2 permissions are allowed for a month")
		
	@frappe.whitelist()
	def get_ceo(self):
		ceo = frappe.db.get_value('Department',self.department,"ceo")
		return ceo
	
	@frappe.whitelist()
	def get_gm(self):
		gm = frappe.db.get_value('Department',self.department,"gm")
		return gm

	@frappe.whitelist()
	def get_hod(self):
		hod = frappe.db.get_value('Department',self.department,"hod")
		return hod
	
	def after_insert(self):
		if self.workflow_state == 'Pending for HOD':
			link = get_url_to_form("Permission Request", self.name)
			content="""<p>Dear Sir,</p>
			Kindly find the below Permission Request from %s (%s).<br>"""%(self.employee,self.employee_name)
			table = """<table class=table table-bordered><tr><th colspan='4' style = 'border: 1px solid black;background-color:#ffedcc;'><center>PERMISSION REQUEST</center></th><tr>
			<tr><th style = 'border: 1px solid black'>Employee ID</th><td style = 'border: 1px solid black'>%s</td><th style = 'border: 1px solid black'>Department</th><td style = 'border: 1px solid black'>%s</td></tr>
			<tr><th style = 'border: 1px solid black'>Employee Name</th><td style = 'border: 1px solid black'>%s</td><th style = 'border: 1px solid black'>Designation</th><td style = 'border: 1px solid black'>%s</td></tr>
			<tr><th style = 'border: 1px solid black'>Permission Date</th><td style = 'border: 1px solid black'>%s</td><th style = 'border: 1px solid black'>Session</th><td style = 'border: 1px solid black'>%s</td></tr>
			<tr><th style = 'border: 1px solid black'>Shift</th><td style = 'border: 1px solid black'>%s</td><th style = 'border: 1px solid black'>From Time</th><td style = 'border: 1px solid black'>%s</td></tr>
			<tr><th rowspan='2' style = 'border: 1px solid black'>Reason</th><td rowspan='2' style = 'border: 1px solid black'>%s</td><th style = 'border: 1px solid black'>To Time</th><td style = 'border: 1px solid black'>%s</td></tr>
			<tr><th style = 'border: 1px solid black'>Hours</th><td style = 'border: 1px solid black'>%s</td></tr>
			<tr><th colspan='4' style = 'border: 1px solid black;background-color:#ffedcc;'><center><a href='%s'>VIEW</a></center></th></tr>
			</table><br>"""%(self.employee,self.department,self.employee_name,self.designation,format_datetime(self.attendance_date),self.session,self.shift,self.from_time,self.reason,self.to_time,self.hours,link)
			regards = "Thanks & Regards,<br>hrPRO"
			frappe.sendmail(
			recipients=[self.permission_approver,'mohan.pan@thaisummit.co.in'],
			subject='Reg.Permission Request Approval' ,
			message = content+table+regards)