# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Approval(Document):
	@frappe.whitelist()
	def submit_doc(self,doctype,name,workflow_state):
		doc = frappe.get_doc(doctype,name)
		doc.workflow_state = workflow_state
		doc.save(ignore_permissions=True)
		doc.submit()
		return "ok"