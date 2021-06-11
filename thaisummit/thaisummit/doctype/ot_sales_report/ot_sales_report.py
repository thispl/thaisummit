# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, add_days, date_diff, getdate
from frappe import _
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from frappe.utils.file_manager import get_file
from frappe.model.document import Document
from datetime import date, timedelta, datetime

class OTSalesReport(Document):
    pass

@frappe.whitelist()
def get_ot_amt(doc,depts,group):
    data = '<td rowspan="%s">%s</td>'%(len(depts)+3,group)
    no_of_days = date_diff(add_days(doc.to_date, 1), doc.from_date)
    dates = [add_days(doc.from_date, i) for i in range(0, no_of_days)]
    for dept in depts:
        data += '<td style="background-color:#FFFF00">%s</td>'%dept
        for date in dates:
            hrs = frappe.db.get_value("Timesheet",{"start_date":date,'end_date':date,"Department":dept},"total_hours") or 0.0
            data += "<td>%s</td>"%hrs
        data = '<tr>' + data + '</tr>'
    return data

@frappe.whitelist()
def get_ot_total(doc,depts):
    no_of_days = date_diff(add_days(doc.to_date, 1), doc.from_date)
    dates = [add_days(doc.from_date, i) for i in range(0, no_of_days)]
    data = '<td style="background-color:#27ae60">OT Amount</td>'
    sales_amount = '<td style="background-color:#d4efdf">Sales Amount</td>'
    per_head = '<td style="background-color:#6495ED">OT %</td>'
    for date in dates:
        hrs = frappe.db.get_value("Timesheet",{"start_date":date,'end_date':date,"Department":['in',depts]},"total_hours") or 0.0
        data += '<td style="background-color:#27ae60">%s</td>'%hrs
        amt = frappe.db.get_value('Sales Amount Per Day', {
        'department': ['in', depts],
        'date': date
    }, 'sum(sales_amount)') or 0.0
        sales_amount += '<td style="background-color:#d4efdf">%s</td>'%amt
        try:
            ph_amt = round((hrs/amt)*100,2)
        except:
            ph_amt = '0.0%'
        per_head += '<td style="background-color:#6495ED">%s</td>'%ph_amt
    data = '<tr>' + data + '</tr><tr>' + sales_amount + '</tr><tr>' + ph_amt +'</tr>'
    return data
