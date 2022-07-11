# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, nowtime
import datetime
from datetime import datetime, time, timedelta
import pandas as pd

class WindowOUT(Document):
	@frappe.whitelist()
	def get_invoices(self):
		invs = frappe.get_all('TSAI Invoice',{'window_status':'IN'},['*'])
		data = []
		for inv in invs:
			std_out_time = round((inv.total_bin*20)/60 + 20)
			planned_out = inv.actual_in_time + timedelta(minutes=std_out_time)
			row = [inv.supplier_name,inv.name,std_out_time,inv.actual_in_time,planned_out]
			data.append(row)
		return data
	
	# @frappe.whitelist()
	# def get_delay(self,child):
	# 	in_time = datetime.strptime(child["actual_in_time"], '%H:%M:%S')
	# 	out_time = datetime.strptime(child["actual_out_time"], '%H:%M:%S')
	# 	duration = 0
	# 	if in_time < out_time:
	# 		duration = (out_time - in_time).seconds/60
	# 	return duration

	@frappe.whitelist()
	def record_out_data(self,row):
		doc = frappe.get_doc('TSAI Invoice',row["invoice_no"])
		# doc.status = 'CLOSED'
		planned_out_time = pd.to_datetime(row['planned_out_time']).time()
		# in_time = datetime.strptime(str(in_time), '%H:%M:%S').time()
		planned_out_time = datetime.combine(pd.datetime.now().date(),planned_out_time)
		out_time = pd.datetime.now().time()
		out_time = datetime.combine(pd.datetime.now().date(),out_time)
		# out_time = datetime.strptime(str(out_time), '%H:%M:%S').time()

		out_delay = (out_time - planned_out_time).seconds/60
		if planned_out_time > out_time:
			out_delay = 0
		doc.std_outtime = row['std_out_time']
		doc.planned_out_time = row['planned_out_time']
		doc.actual_out_time = nowtime()
		doc.outdelay = out_delay
		doc.window_status = 'OUT'
		doc.vehicle_no = self.vehicle_no
		doc.out_bin = row['out_bin']
		try:
			remarks = row['remarks']
		except:
			remarks = ''
		doc.remarks = remarks
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		return 'OK'