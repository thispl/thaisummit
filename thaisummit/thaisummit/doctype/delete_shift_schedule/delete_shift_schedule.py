# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DeleteShiftSchedule(Document):
	pass

@frappe.whitelist()
def delete_shift(department,from_date):
	sa_list = frappe.db.sql("select name from `tabShift Assignment` where start_date = '%s' and department = '%s' "%(from_date,department),as_dict=True)
	if sa_list:
		for sa in sa_list:
			doc = frappe.get_doc("Shift Assignment",sa.name)
			if doc.docstatus == 1:
				doc.cancel()
				frappe.delete_doc("Shift Assignment",doc.name)
			elif doc.docstatus == 0:
				frappe.delete_doc("Shift Assignment",doc.name)
			else:
				frappe.delete_doc("Shift Assignment",doc.name)
		frappe.msgprint('Shift Schedule Deleted Successfully')
	else:
		frappe.msgprint('No Shift Schedule found')

@frappe.whitelist()
def delete_all_shift(from_date):
	sa_list = frappe.db.sql("select name from `tabShift Assignment` where start_date = '%s' "%(from_date),as_dict=True)
	if sa_list:
		for sa in sa_list:
			doc = frappe.get_doc("Shift Assignment",sa.name)
			if doc.docstatus == 1:
				doc.cancel()
				frappe.delete_doc("Shift Assignment",doc.name)
			elif doc.docstatus == 0:
				frappe.delete_doc("Shift Assignment",doc.name)
			else:
				frappe.delete_doc("Shift Assignment",doc.name)
		frappe.msgprint('Shift Schedule Deleted Successfully')
	else:
		frappe.msgprint('No Shift Schedule found')
