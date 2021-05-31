# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, cint, add_months, date_diff, add_days

class ShiftScheduleStatusSummary(Document):
	pass

@frappe.whitelist()
def get_shift_status(doc):
	dates = get_dates(doc.from_date,doc.to_date)
	depts = frappe.get_all("Department",{'is_group':0})
	d_list = ''
	date_list = '<table class="table table-bordered"><tr><th colspan="7"><center>Shift Schedule Status Summary</center></th></tr><tr><td rowspan="2"><center>Department</center></td><td style="background-color:#f1f723">From Date</td><td colspan="2" style="background-color:#e0f3f2"><center>%s</center></td><td style="background-color:#f1f723">To Date</td><td colspan="2" style="background-color:#e0f3f2"><center>%s</center></td></tr><tr><td><center>%s</center></td><td><center>%s</center></td><td><center>%s</center></td><td><center>%s</center></td><td><center>%s</center></td><td><center>%s</center></td></tr>'%(frappe.utils.format_date(doc.from_date),frappe.utils.format_date(doc.to_date),frappe.utils.format_date(dates[0]),frappe.utils.format_date(dates[1]),frappe.utils.format_date(dates[2]),frappe.utils.format_date(dates[3]),frappe.utils.format_date(dates[4]),frappe.utils.format_date(dates[5]))
	for d in depts:
		date1 = frappe.db.sql("select name,workflow_state from `tabShift Schedule` where department = '%s' and '%s' between from_date and to_date and workflow_state != 'Rejected' order by creation desc"%(d.name,dates[0]),as_dict=True)
		date2 = frappe.db.sql("select name,workflow_state from `tabShift Schedule` where department = '%s' and '%s' between from_date and to_date and workflow_state != 'Rejected' order by creation desc"%(d.name,dates[1]),as_dict=True)
		date3 = frappe.db.sql("select name,workflow_state from `tabShift Schedule` where department = '%s' and '%s' between from_date and to_date and workflow_state != 'Rejected' order by creation desc"%(d.name,dates[2]),as_dict=True)
		date4 = frappe.db.sql("select name,workflow_state from `tabShift Schedule` where department = '%s' and '%s' between from_date and to_date and workflow_state != 'Rejected' order by creation desc"%(d.name,dates[3]),as_dict=True)
		date5 = frappe.db.sql("select name,workflow_state from `tabShift Schedule` where department = '%s' and '%s' between from_date and to_date and workflow_state != 'Rejected' order by creation desc"%(d.name,dates[4]),as_dict=True)
		date6 = frappe.db.sql("select name,workflow_state from `tabShift Schedule` where department = '%s' and '%s' between from_date and to_date and workflow_state != 'Rejected' order by creation desc"%(d.name,dates[5]),as_dict=True)
		if date1:
			if date1[0].workflow_state == 'Approved':
				mark1 = '<td style="background-color:#7dcea0">✓</td>'
			elif date1[0].workflow_state == 'Approval Pending':
				mark1 = '<td style="background-color:#f0b27a">-</td>'
		else:
			mark1 = '<td style="background-color:#f95848">X</td>'
		if date2:
			if date2[0].workflow_state == 'Approved':
				mark2 = '<td style="background-color:#7dcea0">✓</td>'
			elif date2[0].workflow_state == 'Approval Pending':
				mark2 = '<td style="background-color:#f0b27a">-</td>'
		else:
			mark2 = '<td style="background-color:#f95848">X</td>'
		if date3:
			if date3[0].workflow_state == 'Approved':
				mark3 = '<td style="background-color:#7dcea0">✓</td>'
			elif date3[0].workflow_state == 'Approval Pending':
				mark3 = '<td style="background-color:#f0b27a">-</td>'
		else:
			mark3 = '<td style="background-color:#f95848">X</td>'
		if date4:
			if date4[0].workflow_state == 'Approved':
				mark4 = '<td style="background-color:#7dcea0">✓</td>'
			elif date4[0].workflow_state == 'Approval Pending':
				mark4 = '<td style="background-color:#f0b27a">-</td>'
		else:
			mark4 = '<td style="background-color:#f95848">X</td>'
		if date5:
			if date5[0].workflow_state == 'Approved':
				mark5 = '<td style="background-color:#7dcea0">✓</td>'
			elif date5[0].workflow_state == 'Approval Pending':
				mark5 = '<td style="background-color:#f0b27a">-</td>'
		else:
			mark5 = '<td style="background-color:#f95848">X</td>'
		if date6:
			if date6[0].workflow_state == 'Approved':
				mark6 = '<td style="background-color:#7dcea0">✓</td>'
			elif date6[0].workflow_state == 'Approval Pending':
				mark6 = '<td style="background-color:#f0b27a">-</td>'
		else:
			mark6 = '<td style="background-color:#f95848">X</td>'
		
		d_list += '<tr><td>%s</td>%s%s%s%s%s%s<tr>'%(d.name,mark1,mark2,mark3,mark4,mark5,mark6)
	data = date_list + d_list + '</table>'
	frappe.errprint(data)
	return data

def get_dates(from_date,to_date):
    """get list of dates in between from date and to date"""
    no_of_days = date_diff(add_days(to_date, 1),from_date )
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates
