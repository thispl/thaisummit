# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.file_manager import get_file
from frappe.model.document import Document
from datetime import datetime
from frappe.utils.xlsxutils import read_xlsx_file_from_attached_file
import pandas as pd
from frappe.utils.background_jobs import enqueue



class IYMSequencePlanUpload(Document):
	@frappe.whitelist()
	def before_submit(self):
		file = get_file(self.attach)
		pps = read_xlsx_file_from_attached_file(fcontent=file[1])
		for pp in pps:
			if pp[0] not in ('ASSY LINE-A','Date'):
				frappe.db.sql("delete from `tabIYM Sequence Plan` where date = '%s' "%pp[0])
				frappe.db.sql("delete from `tabTSA Master` where date = '%s' "%pp[0])
				# plans = frappe.get_all('IYM Sequence Plan',{'date':pp[0]})
				# for p in plans:
				# 	frappe.delete_doc('IYM Sequence Plan',p.name)
				doc = frappe.new_doc("IYM Sequence Plan")
				if pp[2]:
					if pp[0] not in ('ASSY LINE-A','Date'):
						if not frappe.db.exists('Model Number',pp[4].replace("'","")):
							mod = frappe.new_doc("Model Number")
							mod.model_number = pp[4].replace("'","")
							mod.model_barcode = pp[4].replace("'","")
							mod.save(ignore_permissions=True)
						if pp[0]:
							date = pd.to_datetime(pp[0]).date()
						if pp[1]:
							assy_line = pp[1]
						doc.date = date
						doc.assy_line_type = 'A'
						doc.assy_line = assy_line
						doc.assy_plan_date = pd.to_datetime(pp[2]).date()
						doc.model_code = pp[4].replace("'","")
						doc.parts_qty = pp[8]
						doc.weld_plan_qty = pp[19]
						if pp[21]:
							doc.weld_recv_status = 'Completed'
						else:
							if pp[19]:
								doc.weld_recv_status = 'Pending'
							else:
								doc.weld_recv_status = 'Not Required'
						doc.aced_plan_qty = pp[22]
						if pp[24]:
							doc.aced_recv_status = 'Completed'
						else:
							if pp[22]:
								doc.aced_recv_status = 'Pending'
							else:
								doc.aced_recv_status = 'Not Required'
						doc.fuel_plan_qty = pp[25]
						if pp[27]:
							doc.fuel_recv_status = 'Completed'
						else:
							if pp[25]:
								doc.fuel_recv_status = 'Pending'
							else:
								doc.fuel_recv_status = 'Not Required'
						doc.assy_plan_qty = pp[28]
						if pp[30]:
							doc.assy_recv_status = 'Completed'
						else:
							if pp[28]:
								doc.assy_recv_status = 'Pending'
							else:
								doc.assy_recv_status = 'Not Required'
						doc.upload_ref = self.name
						doc.save(ignore_permissions=True)
						frappe.db.commit()
				elif pp[11]:
					if pp[0] not in ('ASSY LINE-A','Date'):
						if not frappe.db.exists('Model Number',pp[13].replace("'","")):
							mod = frappe.new_doc("Model Number")
							mod.model_number = pp[13].replace("'","")
							mod.model_barcode = pp[13].replace("'","")
							mod.save(ignore_permissions=True)
						if pp[0]:
							date = pd.to_datetime(pp[0]).date()
							# date = datetime.strptime(pp[0],'%m/%d/%Y')
						if pp[10]:
							assy_line = pp[10]
						doc.date = date
						doc.assy_line_type = 'B'
						doc.assy_line = assy_line
						# try:
						doc.assy_plan_date = pd.to_datetime(pp[11]).date()
							# doc.assy_plan_date = datetime.strptime(pp[11],'%Y-%m-%d')
						# except:
							# doc.assy_plan_date = datetime.strptime(pp[11],'%m/%d/%Y')
						doc.model_code = pp[13].replace("'","")
						doc.parts_qty = pp[17]
						doc.weld_plan_qty = pp[19]
						if pp[21]:
							doc.weld_recv_status = 'Completed'
						else:
							if pp[19]:
								doc.weld_recv_status = 'Pending'
							else:
								doc.weld_recv_status = 'Not Required'
						doc.aced_plan_qty = pp[22]
						if pp[24]:
							doc.aced_recv_status = 'Completed'
						else:
							if pp[22]:
								doc.aced_recv_status = 'Pending'
							else:
								doc.aced_recv_status = 'Not Required'
						doc.fuel_plan_qty = pp[25]
						if pp[27]:
							doc.fuel_recv_status = 'Completed'
						else:
							if pp[25]:
								doc.fuel_recv_status = 'Pending'
							else:
								doc.fuel_recv_status = 'Not Required'
						doc.assy_plan_qty = pp[28]
						if pp[30]:
							doc.assy_recv_status = 'Completed'
						else:
							if pp[28]:
								doc.assy_recv_status = 'Pending'
							else:
								doc.assy_recv_status = 'Not Required'
						doc.upload_ref = self.name
						doc.save(ignore_permissions=True)
						frappe.db.commit()