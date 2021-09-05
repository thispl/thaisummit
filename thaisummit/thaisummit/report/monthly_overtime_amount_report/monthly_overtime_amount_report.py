# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt
import frappe
from datetime import date, timedelta
from frappe import msgprint, _
from frappe.utils import cstr, cint, getdate
from frappe.utils import cstr, add_days, date_diff, getdate
from datetime import date, timedelta, datetime

def execute(filters=None):
    columns = get_columns(filters)
    data = get_amount(filters)
    return columns,data

def get_columns(filters):
	coloumn = [_("Department" + ":Data/:200")]
	no_of_days = date_diff(filters.from_date,filters.to_date)
	dates = [add_days(filters.from_date,i) for i in range(0,no_of_days)]
	

def get_amount(filters):
