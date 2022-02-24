# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TSAISupplier(Document):
    def after_insert(self):
        user = frappe.new_doc('User')
        user.email = self.email
        user.first_name = self.supplier_name
        user.username = self.name
        user.new_password = str(self.name) + '@123'
        user.send_welcome_email = 0
        user.save(ignore_permissions=True)
        frappe.db.commit()
        self.user_name = self.name
        self.user = user.name
        doc = frappe.get_doc('User',user.name)
        doc.add_roles('Supplier')
        doc.save(ignore_permissions=True)
        frappe.db.commit()