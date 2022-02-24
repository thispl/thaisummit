# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from six import string_types
import frappe
import json
from frappe.utils import date_diff, add_months, today, getdate, add_days, flt, get_last_day, get_first_day, cint, get_link_to_form, rounded
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime, time, timedelta
import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate


def execute(filters=None):
	columns, data = [] ,[]
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	column = [
		_('Departemnt') + ':Data:120',
		_(add_days(today(), -2)) + ':Data:120',
		_(add_days(today(), -1)) + ':Data:120',
		_(today()) + ':Data:120',
		_(add_days(today(), 1)) + ':Data:120',
		_(add_days(today(), 2)) + ':Data:120',
	]	
	return column

def get_data(filters):
	data = []
	department = frappe.db.get_all('Department')
	for d in department:
		count1 = frappe.db.sql(""" select count(*) as count1 from `tabLeave Application` where department='%s'  and '%s' between from_date and to_date """ % (d.name,add_days(today(),-2)),as_dict=True)[0].count1
		count2 = frappe.db.sql(""" select count(*) as count2 from `tabLeave Application` where department='%s'  and '%s' between from_date and to_date """ % (d.name,add_days(today(),-1)),as_dict=True)[0].count2
		count3 = frappe.db.sql(""" select count(*) as count3 from `tabLeave Application` where department='%s'  and '%s' between from_date and to_date """ % (d.name,add_days(today(),0)),as_dict=True)[0].count3
		count4 = frappe.db.sql(""" select count(*) as count4 from `tabLeave Application` where department='%s'  and '%s' between from_date and to_date """ % (d.name,add_days(today(),1)),as_dict=True)[0].count4
		count5 = frappe.db.sql(""" select count(*) as count5 from `tabLeave Application` where department='%s'  and '%s' between from_date and to_date """ % (d.name,add_days(today(),2)),as_dict=True)[0].count5

		row = [d.name,count1,count2,count3,count4,count5]
		data.append(row)
	return data	

