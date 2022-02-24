# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import cstr, add_days, date_diff, getdate
import datetime
from datetime import datetime

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = ['MAT NO','PART NO','PART NAME','CUS']
	no_of_days = date_diff(add_days(filters.to_date, 1), filters.from_date)
	dates = [add_days(filters.from_date, i) for i in range(0, no_of_days)]
	for date in dates:
		date = datetime.strptime(str(date),'%Y-%m-%d')
		d = date.strftime('%d')
		m = date.strftime('%b')
		columns.append(d + '-' + m)
	return columns
	
def get_data(filters):
	data = []

	no_of_days = date_diff(add_days(filters.to_date, 1), filters.from_date)
	dates = [add_days(filters.from_date, i) for i in range(0, no_of_days)]

	parts = frappe.get_all('TSAI Part Master',['*'],order_by="mat_no")
	for p in parts:
		row = [p.mat_no,p.parts_no,p.parts_name,p.customer]
		for date in dates:
			q = frappe.db.get_value('Forecast Data',{'mat_no':p.mat_no,'date':date},'qty') or '-'
			row.append(q)
		data.append(row)
	return data