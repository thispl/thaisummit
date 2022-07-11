# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import datetime

class CLReturn(Document):
    
    @frappe.whitelist()
    def new_cl_return_form(self):
        for cl_return in self.cl_returns_entry:
            cl = frappe.new_doc('CL Return Form')
            cl.date = self.date
            cl.time = self.time
            cl.enter_id = cl_return.employee_id
            cl.employee_name = cl_return.employee_name
            cl.department = cl_return.department
            cl.remarks = cl_return.remarks
            cl.save(ignore_permissions=True)
            frappe.db.commit()