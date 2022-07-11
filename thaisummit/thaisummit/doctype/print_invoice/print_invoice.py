# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PrintInvoice(Document):
    pass

@frappe.whitelist()
def get_supplier_invoice(from_date,to_date,supplier=None):
    if 'System Manager' not in frappe.get_roles(frappe.session.user):
        if 'Supplier' in frappe.get_roles(frappe.session.user):
            supplier_code = frappe.db.get_value('TSAI Supplier',{'email':frappe.session.user},'name')
            invs = frappe.db.sql("""select name, invoice_date, supplier_name from `tabTSAI Invoice` where invoice_date between '%s' and '%s' and supplier_code = '%s' """%(from_date,to_date,supplier_code),as_dict=True)
            return invs
    else:
        if supplier:
            invs = frappe.db.sql("""select name, invoice_date,supplier_name from `tabTSAI Invoice` where invoice_date between '%s' and '%s' and supplier_code = '%s' """%(from_date,to_date,supplier),as_dict=True)
            return invs