# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class TAGCancel(Document):
	@frappe.whitelist()
	def make_as_cancel(self,receipt_entry):
		for row in receipt_entry:
			tag_master =frappe.db.sql("""select name,recieved_time from `tabTAG Master` where  parts_no = '%s' and required_quantity = '%s' and item_delivered = 0 and delivery_status != 'Cancelled' order by name""" %(row["parts_no"],row["quantity"]),as_dict=True)[0]
			update_master = frappe.get_doc("TAG Master",tag_master.name)
			update_master.delivery_status = "Cancelled"
			update_master.save(ignore_permissions=True)
			frappe.db.commit()
		return "Tag Masters Cancelled Successfully"
