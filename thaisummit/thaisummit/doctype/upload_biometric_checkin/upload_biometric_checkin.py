# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.csvutils import read_csv_content
from frappe.utils.file_manager import get_file
from datetime import datetime,timedelta,date,time

class UploadBiometricCheckin(Document):
	def error_preview(self):
		filepath = get_file(self.attach)
		pps = read_csv_content(filepath[1])
		errs = '<h2>Error Checkins </h2><table class="table table-bordered"><tr><td style="background-color:#f0b27a; border: 1px solid black">Row No.</td><td style="background-color:#f0b27a; border: 1px solid black">Employee ID</td><td style="background-color:#f0b27a; border: 1px solid black">Error</td><tr>'
		i = 1
		rows = 1
		err_rows = 1
		for pp in pps:
			if pp[5] != 'Employee Name':
				if pp[5]:
					if not frappe.db.exists("Employee",pp[5]):
						errs += '<tr><td style="border: 1px solid black">%s</td><td style="border: 1px solid black">%s</td><td style="border: 1px solid black">Employee not found</td></tr>'%(i,pp[5])
						err_rows += 1
					rows += 1
			i += 1
		count = '<h2>Summary</h2><table class="table table-bordered"><tr><td style="background-color:#f0b27a; border: 1px solid black">Total Checkins</td><td style="border: 1px solid black">%s</td><td style="background-color:#f0b27a; border: 1px solid black">Valid Checkins</td><td style="border: 1px solid black">%s</td><td style="background-color:#f0b27a; border: 1px solid black">Invalid Checkins</td><td style="border: 1px solid black">%s</td></tr></table>'%(rows,rows-err_rows,err_rows)
		data = count + errs + '</table>'
		return data
	
@frappe.whitelist()
def create_checkins(file,name):
	filepath = get_file(file)
	pps = read_csv_content(filepath[1])
	for pp in pps:
		if frappe.db.exists("Employee",pp[5]):
			frappe.errprint(pp[5])
			t = datetime.strptime(pp[1], '%d-%b-%Y %H:%M:%S')
			if not frappe.db.exists("Employee Checkin",{'employee':pp[5],'time':t}):
				frappe.errprint(pp[1])
				doc = frappe.new_doc("Employee Checkin")
				doc.employee = pp[5]
				doc.time = t
				doc.log_type = pp[2].upper()
				doc.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.errprint(doc)
	ubc = frappe.get_doc("Upload Biometric Checkin",name)
	ubc.submit()
	frappe.db.commit()