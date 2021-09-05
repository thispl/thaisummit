# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	row = get_departments(filters)
	for r in row:
		data.append(r)
	return columns, data

def get_columns():
    columns = [
        _("Department") + ":Data:200",
		_("From Date") + ":Date:100",
		_("To Date") + ":Date:100",
        _("Status") + ":Data:120",
    ]
    return columns

def get_departments(filters):
	row = []
	departments = frappe.get_all("Department",{'is_group':0})
	for dept in departments:
		ss = frappe.db.sql("select count(*) as count, from_date, to_date from `tabShift Schedule` where department = '%s' and from_date between '%s' and '%s' and workflow_state != 'Rejected' "%(dept.name,filters.from_date,filters.to_date),as_dict=True)
		if ss[0].count != 0:
			row += [[dept.name,ss[0].from_date,ss[0].to_date,"Applied"]]
		else:
			row += [[dept.name,ss[0].from_date,ss[0].to_date,"Not Applied"]]
	return row
