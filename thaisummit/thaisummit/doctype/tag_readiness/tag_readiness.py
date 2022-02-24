# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TagReadiness(Document):
    @frappe.whitelist()
    def update_readiness(self):
        for tru in self.tag_readiness_update:
            frappe.errprint(tru.tag_master)
            tm = frappe.get_doc("TAG Master",tru.tag_master)
            tm.readiness_qty = tru.readiness_qty
            tm.save(ignore_permissions=True)
            frappe.db.commit()
        return "Readiness Quantity Updated"
    
    @frappe.whitelist()
    def get_slot_no(self):
        args = frappe.local.form_dict
        return args.slot_no

