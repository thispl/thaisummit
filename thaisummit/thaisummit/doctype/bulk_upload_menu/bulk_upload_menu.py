# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.file_manager import get_file
from frappe.utils.csvutils import UnicodeWriter, read_csv_content

class BulkUploadMenu(Document):

	def on_submit(self):
		filepath = get_file(self.attach)
		pps = read_csv_content(filepath[1])
		for pp in pps:
			doc = frappe.new_doc('Employee Menu Preference')
			doc.date = self.date
			doc.employee = pp[0]
			doc.meal_type = self.meal_type
			doc.save(ignore_permissions=True)
			frappe.db.commit()


	