# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

from unicodedata import name
import frappe
from frappe.model.document import Document

class ShiftChangeRequest(Document):

	def on_submit(self):
		frappe.db.set_value('Shift Assignment',self.shift_marked,'shift_type',self.shift_change)
		
