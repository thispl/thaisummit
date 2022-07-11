# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe import get_request_header, msgprint, _


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
    columns = [_("Mat No") + ":Data/:100", _("Invoice No") + ":Data/:150", _("Supplier Name") + ":Data/:150",  _("Date") + ":Date/:100", _("Qty") + ":Data/:50"]
    return columns


def get_data(filters):
	if filters.mat_no:
		data = []
		invs = frappe.db.sql("""select `tabInvoice Items`.key_qty,`tabTSAI Invoice`.name, `tabTSAI Invoice`.supplier_name,`tabTSAI Invoice`.invoice_date,`tabInvoice Items`.mat_no from `tabTSAI Invoice`
		left join `tabInvoice Items` on `tabTSAI Invoice`.name = `tabInvoice Items`.parent
		where `tabTSAI Invoice`.status = 'OPEN' and `tabInvoice Items`.mat_no = '%s' and `tabInvoice Items`.grn = 0 """ % (filters.mat_no), as_dict=True)
		for inv in invs:
			data.append([inv.mat_no,inv.name,inv.supplier_name,inv.invoice_date,inv.key_qty])
		return data