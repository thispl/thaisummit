# Copyright (c) 2023, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Testdoc(Document):
	# 1st ques
	@frappe.whitelist()
	def sale_order(total):
		sale_order = frappe.get_single('Sales Order Settings').threshold_value
		if total > sale_order:
			frappe.throw(_('Total amount is greater than threshold value'))

	# 14th ques
	@frappe.whitelist()
	def hide_field(emp):
		employee = frappe.db.sql("""select department from `tabEmployee` where employee ='%s' """%(emp),as_dict=1)[0]
		return employee['departments']

	#  17th ques
	@frappe.whitelist()
	def hide_field(value):
		if value < 0
			frappe.throw(_('Invalid value: Please enter a positive integer.'))
		

	# 10th ques
	@frappe.whitelist()
	def set_order_number(doc, method):
    if doc.doctype == "Sales Order":
        now = datetime.now()
        order_number = "ORD-" + now.strftime("%Y%m%d%H%M%S")
        doc.order_number = order_number
	# need to call the method in before_insert of hooks

	
	from frappe.utils import validate_url
	from frappe.utils import flt
	@frappe.whitelist()
	def validate(self):
		# 28 ques
		discount = flt(self.discount)
		total_amount = flt(self.total_amount)
		if discount < 0 or discount > 0.5 * total_amount:
			frappe.throw("Discount must be between 0% and 50% of the total amount.")

		# 22 ques
		if validate_url(self.url):
			frappe.errprint('hi')
		else:
			frappe.throw(_('Invalid URL.'))

	# 30 th ques
	@frappe.whitelist()
	def display_reminder_message():
    	frappe.throw("You have unsaved changes. Are you sure you want to leave this page?")
		# need to call the method in before_save of hooks

	# 20 th ques
	@frappe.whitelist()
	def get_location(pincode):
		location = frappe.db.sql("""select location from `tabPincode` where name ='%s' """%(pincode),as_dict=1)[0]
		return location['location']


		




