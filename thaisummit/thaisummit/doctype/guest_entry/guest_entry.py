# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import cstr

class GuestEntry(Document):
	
	def validate(self):
		allowed_items = []
		amount = [self.bf_amount,self.lbv_amount,self.lbnv_amount,self.lsv_amount,self.lsnv_amount,self.dbv_amount,self.dbnv_amount,self.dsv_amount,self.dsnv_amount,self.sd_amount,self.ssf_amount]
		total =  sum(amount)
		self.total_amount = total
		
		if self.break_fast:
			allowed_items.append('Break Fast')

		if self.lunch_briyani_veg or self.lunch_briyani_non_veg or self.lunch_special_veg or self.lunch_special_non_veg:
			allowed_items.append('Lunch')

		if self.dinner_briyani_veg or self.dinner_briyani_non_veg or self.dinner_special_veg or self.dinner_special_non_veg:
			allowed_items.append('Dinner')

		if self.supper_dates or self.supper_special_food:
			allowed_items.append('Supper')

		self.allowed_items = cstr(allowed_items)