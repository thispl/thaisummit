# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe 
from frappe import msgprint, _


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns =[]
	columns += [
		_("Supplier Name")+":Data:150",
		_("Invoice No")+":Data:150",
		_("Status")+":Data:100",
		_("Invoice Date")+":Date:100",
		_("MAT No")+":Data:100",
		_("Part NO")+":Data:100",
		_("Part Name")+":Data:150",
		_("QTY")+":Data:75",
		_("Rate")+":Data:75",
		_("Basic Amount")+":Data:120",
		_("Invoice Amount")+":Data:120",
		_("GRN Date")+":Date:100",
        _("GRN No")+":Data:100",
        _("GRN QTY")+":Data:100",
        _("GRN Amount")+":Data:120",
	]
	return columns
def get_data(filters):
	data =[]
	supplier_code = frappe.db.get_value('TSAI Supplier',{'email':frappe.session.user},'name')
	if supplier_code:
		invoices = frappe.get_all("TSAI Invoice",{"invoice_date": ("between",(filters.from_date,filters.to_date)),'supplier_code':supplier_code},['*']) 
	else:
		if 'E-Kanban User' in frappe.get_roles(frappe.session.user):
			invoices = frappe.get_all("TSAI Invoice",{"invoice_date": ("between",(filters.from_date,filters.to_date))},['*'])
	for inv in invoices:
		invoice_items = frappe.get_all("Invoice Items",{"parent":inv.name},["*"])
		for item in invoice_items:
			if inv.status in ('OPEN','CLOSED'):
				status = '-'
			else:
				status = inv.status
			row = [inv.supplier_name,inv.name,status,inv.invoice_date,item.mat_no,item.parts_no,item.parts_name,item.key_qty,item.unit_price,item.basic_amount,item.invoice_amount,item.grn_date,item.grn_no,item.grn_qty,item.basic_amount]
			data.append(row)
	return data