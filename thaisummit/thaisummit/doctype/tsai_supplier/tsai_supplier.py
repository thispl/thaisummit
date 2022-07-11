# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TSAISupplier(Document):
    def validate(self):
        if not self.is_new():
            doc = frappe.get_doc('User',self.email)
            if self.enabled == 1:
                doc.enabled = 1
            elif self.enabled == 0:
                doc.enabled = 0
            doc.save(ignore_permissions=True)
            frappe.db.commit()

    def after_insert(self):
        user = frappe.new_doc('User')
        user.email = self.email
        user.first_name = self.supplier_name
        user.username = self.name
        user.new_password = str(self.name) + '@123'
        user.send_welcome_email = 0
        user.save(ignore_permissions=True)
        frappe.db.commit()
        doc = frappe.get_doc('User',user.name)
        # doc.add_roles('Supplier')
        doc.role_profile_name = "Supplier"
        # doc.module_profile = "Supplier"
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        doc = frappe.get_doc('User',user.name)
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        up = frappe.new_doc('User Permission')
        up.user = user.name
        up.allow = "TSAI Supplier"
        up.for_value = self.name
        up.save(ignore_permissions=True)
        frappe.db.commit()
        self.validate()