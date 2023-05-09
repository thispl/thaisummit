# Copyright (c) 2023, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeProductionLineDetails(Document):
    def validate(self):
        user = frappe.session.user
        if user != 'Administrator':
            user_list = frappe.db.sql("""select name from `tabUser` where name = '%s' """ % (self.user_id), as_dict=1)[0]
            if user_list['name']:
                frappe.get_doc('User', self.user_id).add_roles(self.role)
                frappe.msgprint("Role has been updated successfully.")



