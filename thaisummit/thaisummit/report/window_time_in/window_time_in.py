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
		_("Supplier Name")+":Data:200",
		_("Date")+":Date:150",
		_("Invoice No")+":Data:100",
		_("No of Bins")+":Data:120",
		_("Amount")+":Data:150",
		_("STD IN Time")+":Time:150",
		_("Actual IN Time")+":Time:150",
		_("Delay(Mins")+":Data:100",

	]
	return columns

def get_data(filters):
	data =[]
	invoices = frappe.get_all("TSAI Invoice",{"invoice_date": ("between",(filters.from_date,filters.to_date)),'window_status':'IN'},['*']) 
	for inv in invoices:
		row = [inv.supplier_name,inv.invoice_date,inv.name,inv.total_bin,inv.total_invoice_amount,inv.std_in_time,inv.actual_in_time,inv.delaymins]
		data.append(row)
	return data