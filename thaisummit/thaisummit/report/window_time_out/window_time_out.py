# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns =[]
	columns += [
		_("Invoice No")+":Data:200",
		_("Supplier Name")+":Data:200",
		_("STD OUT Time(Mins)")+":Data:150",
		_("Actual OUT Time")+":Time:150",
		_("Planned OUT Time")+":Time:150",
		_("Delay(Mins)")+":Data:150",
		_("No of Bins")+":Data:120",

	]
	return columns

def get_data(filters):
	data =[]
	invoices = frappe.get_all("TSAI Invoice",{"invoice_date": ("between",(filters.from_date,filters.to_date)),'window_status':'OUT'},['*']) 
	for inv in invoices:
		row = [inv.name,inv.supplier_name,inv.std_outtime,inv.actual_out_time,inv.planned_out_time,inv.outdelay,inv.out_bin]
		data.append(row)
	return data
