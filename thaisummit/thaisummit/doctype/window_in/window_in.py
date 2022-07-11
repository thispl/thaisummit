# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

from wsgiref.simple_server import demo_app
import frappe
from frappe.model.document import Document
from frappe.utils import today, nowtime
import datetime
from datetime import datetime

class WindowIN(Document):
	@frappe.whitelist()
	def get_invoices(self):
		if not self.supplier:
			invs = frappe.get_all('TSAI Invoice',{'invoice_date':self.date,'window_status':''},['*'])
		else:
			invs = frappe.get_all('TSAI Invoice',{'invoice_date':self.date,'supplier_code':self.supplier,'window_status':''},['*'])
		data = []
		for inv in invs:
			window_time = frappe.db.get_value('TSAI Supplier',inv.supplier_code,'window_time')
			row = [inv.supplier_name,inv.invoice_date,inv.name,inv.total_bin,inv.total_invoice_amount,window_time]
			data.append(row)
		return data
	
	@frappe.whitelist()
	def get_delay(self,child):
		in_time = datetime.strptime(child["actual_in_time"], '%H:%M:%S')
		window_time = datetime.strptime(child["std_in_time"], '%H:%M:%S')
		delay = 0
		if in_time > window_time:
			delay = (in_time - window_time).seconds/60
		return delay

	@frappe.whitelist()
	def record_in_data(self,row):
		doc = frappe.get_doc('TSAI Invoice',row["invoice_no"])
		# doc.status = 'CLOSED'
		doc.std_in_time = row["std_in_time"]
		doc.actual_in_time = nowtime()
		in_time = datetime.strptime(row["std_in_time"], '%H:%M:%S')
		out_time = datetime.now().time().strftime('%H:%M:%S')
		out_time = datetime.strptime(out_time, '%H:%M:%S')
		doc.delaymins = (out_time - in_time).seconds/60
		doc.window_status = 'IN'
		doc.gate_in_date = today()
		doc.std_out_time = '00:00'
		doc.actual_out_time = '00:00'
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		return 'OK'

