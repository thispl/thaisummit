# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import timedelta,datetime
from frappe.utils import cint, getdate, get_datetime

class TAGOUT(Document):
	@frappe.whitelist()
	def make_as_delivery(self,receipt_entry):
		for row in receipt_entry:
			# part_no =frappe.get_value('Part Master',{'parts_no':row["parts_no"]},'name')
			tag_master =frappe.db.sql("""select name,recieved_time from `tabTAG Master` where  parts_no = '%s' and required_quantity = '%s' and item_delivered = 0 and delivery_status != 'Cancelled' order by name""" %(row["parts_no"],row["quantity"]),as_dict=True)[0]
			master_name = tag_master.name
			status = 'On Time Sent'
			delay = frappe.db.get_value("TAG Monitoring Management",None,"delay_duration")
			tag_master_time = datetime.strptime(str(tag_master.recieved_time), '%Y-%m-%d %H:%M:%S')
			submission_time = datetime.now()
			time_taken = submission_time - tag_master_time
			allowed_delay_duration = timedelta(seconds=cint(delay))
			if time_taken > allowed_delay_duration:
				status = 'Delay'
			update_master = frappe.get_doc("TAG Master",tag_master.name)
			update_master.item_delivered = 1
			update_master.vehicle_out = self.vehicle
			update_master.date_and_time = datetime.now()
			update_master.delivery_status = 'Delivered'
			update_master.sent = status
			update_master.save(ignore_permissions=True)
			frappe.db.commit()
		return "Out Marked Successfully"