import frappe
from frappe.utils import today

@frappe.whitelist()
def get_server_date():
    return today()
