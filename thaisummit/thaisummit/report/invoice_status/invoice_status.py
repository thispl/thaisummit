# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
import json
import requests

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    columns = []
    columns += [
        _("Supplier Name")+":Data:100",
        _("Invoice No")+":Data:100",
        _("Status")+":Data:100",
        _("Invoice Amount")+":Data:120",
        _("Invoice Date")+":Date:120",
        # _("GATE in Date")+":Data:120",
        # _("GATE in Time")+":Data:120",
        _("GRN Date")+":Date:100",
        _("GRN No")+":Data:100",
        # _("GRN QTY")+":Data:100",
        # _("GRN Amount")+":Data:120",
    ]
    return columns


def get_data(filters):
    data = []
    supplier_code = frappe.db.get_value(
        'TSAI Supplier', {'email': frappe.session.user}, 'name')
    if supplier_code:
        invoices = frappe.get_all("TSAI Invoice", {"invoice_date": (
            "between", (filters.from_date, filters.to_date)), 'supplier_code': supplier_code}, ['*'])
    else:
        if 'E-Kanban User' in frappe.get_roles(frappe.session.user):
            invoices = frappe.get_all("TSAI Invoice", {"invoice_date": (
                "between", (filters.from_date, filters.to_date))}, ['*'])
    for inv in invoices:
        grn_details = frappe.db.sql("""select sum(`tabInvoice Items`.grn_qty) as grn_qty, `tabInvoice Items`.grn_no,`tabInvoice Items`.grn_date from `tabTSAI Invoice` left join `tabInvoice Items` on `tabTSAI Invoice`.name = `tabInvoice Items`.parent where `tabTSAI Invoice`.name = '%s' """%(inv.name),as_dict=True)[0]
        
        if inv.status in ('OPEN','CLOSED'):
            status = '-'
        else:
            status = inv.status

        # row = [inv.supplier_name, inv.name, status, inv.total_invoice_amount,
        #             inv.invoice_date, "-", "-",  grn_details.grn_date, grn_details.grn_no, grn_details.grn_qty, "-"]
        row = [inv.supplier_name, inv.name, status, inv.total_invoice_amount,
                    inv.invoice_date,  grn_details.grn_date, grn_details.grn_no]
        data.append(row)
    return data


# def test_method():
#     invoices = frappe.get_all("TSAI Invoice", ['*'])
#     for inv in invoices:
#         invoice_items = frappe.get_all( "Invoice Items", {"parent": inv.name}, ["*"])
#         for item in invoice_items:
#             print (item)
