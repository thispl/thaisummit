# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.xlsxutils import read_xlsx_file_from_attached_file
from frappe.utils.file_manager import get_file
import datetime
from datetime import datetime
import pandas as pd

class GRNUpload(Document):
	def on_submit(self):
		file = get_file(self.attach)
		pps = read_xlsx_file_from_attached_file(fcontent=file[1])
		for pp in pps:
			if pp[0] != 'GRN No':
				try:
					date = pd.to_datetime(str(pp[1])).date()
					# date = datetime.strptime(str(pp[1]),'%d/%m/%Y').date()
					doc = frappe.get_doc('TSAI Invoice',pp[3])
					for row in doc.invoice_items:
						if row.mat_no == int(pp[4]):
							row.grn = 1
							row.grn_no = pp[0]
							row.grn_date = date
							row.grn_qty = pp[5]
					doc.save(ignore_permissions=True)
					frappe.db.commit()
				except:
					frappe.throw("GRN Date should be in dd/mm/yyyy ")
				
