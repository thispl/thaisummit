# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.print_format import download_multi_pdf


class BulkSalarySlipDownload(Document):
    pass


@frappe.whitelist()
def get_slip(start_date, employee_type):
    data = []
    slip = frappe.db.get_list('Salary Slip', {
                              'start_date': start_date, 'employee_type': employee_type, 'docstatus': ('!=', '2')}, ['name'])
    return slip


@frappe.whitelist()
def get_pdf_link():
    doctype = dict({
        "Salary Slip": ["Sal Slip/TSAI0333/00001"]
    })
    docname = 'SS',
    print_format = 'Salary Slip New',
    no_letterhead = "1"
    download_multi_pdf(doctype, docname, print_format, no_letterhead=1)
