# Copyright (c) 2023, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RMInput(Document):

	@frappe.whitelist()
	def get_old_iym(self):
		rm_price_iym = frappe.get_single('RM Input').rm_input_table1
		# rm_price_re = frappe.get_single('RM Input').rm_input_table2
		for r in rm_price_iym:
			self.append('old_iym_settings',{
				'customer':r.customer,
				'grade':r.grade,
				'std_old':r.std_old,
				'std_impact':r.std_impact,
				'std_new':r.std_new,
				'old1':r.old1,
				'impact1':r.impact1,
				'new1':r.new1,
				'old2':r.old2,
				'impact2':r.impact2,
				'new2':r.new2,
				'coil_old':r.coil_old,
				'coil_impact':r.coil_impact,
				'coil_new':r.coil_new,
				'coil_old1':r.coil_old1,
				'coil_impact1':r.coil_impact1,
				'coil_new1':r.coil_new1,
				'tube_100_old':r.tube_100_old,	
				'tube_100_impact':r.tube_100_impact,
				'tube_100_new':r.tube_100_new,
				'tube_old':r.tube_old,
				'tube_impact':r.tube_impact,
				'tube_new':r.tube_new
	
			})
		self.save()
		# start

	@frappe.whitelist()
	def get_old_re(self):
		for s in self.rm_input_table2:
			self.append('old_re_settings',{
				'customer':s.customer,
				'grade':s.grade,
				'old1':s.old1,
				'impact1':s.impact1,
				'new1':s.new1,
				'old2':s.old2,
				'impact2':s.impact2,
				'new2':s.new2,
				'coil_old':s.coil_old,
				'coil_impact':s.coil_impact,
				'coil_new':s.coil_new,
				'coil_old1':s.coil_old1,
				'coil_impact1':s.coil_impact1,
				'coil_new1':s.coil_new1,
				'tube_100_old':s.tube_100_old,	
				'tube_100_impact':s.tube_100_impact,
				'tube_100_new':s.tube_100_new,
				'tube_old':s.tube_old,
				'tube_impact':s.tube_impact,
				'tube_new':s.tube_new
			})
		self.save()




