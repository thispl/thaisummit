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


class MonthlySalesPerHead(Document):
    pass

@frappe.whitelist()
def get_dates(doc):
    data = ''
    days = ''
    from_date = datetime.strptime(doc.from_date, "%Y-%m-%d")
    to_date = datetime.strptime(doc.to_date, "%Y-%m-%d")
    delta = date_diff(to_date,from_date)
    for i in range(delta + 1):
        day = from_date + timedelta(days=i)
        day_name = day_abbr[getdate(day).weekday()]
        days += '<td>%s-%s</td>'%(cstr(day.day),day_name)
    data = '<tr><td>Date-Day</td>' + days + '</tr>'
    return data

@frappe.whitelist()
def get_att_count(doc,depts):
    data = ''
    no_of_days = date_diff(add_days(doc.to_date, 1), doc.from_date)
    dates = [add_days(doc.from_date, i) for i in range(0, no_of_days)]
    for dept in depts:
        data += '<td style="background-color:#FFFF00">%s</td>'%dept
        for date in dates:
            c = frappe.db.count("Attendance",{"attendance_date":date,'status':'Present',"Department":dept})
            data += "<td>%s</td>"%c
        data = '<tr>' + data + '</tr>'
    return data

@frappe.whitelist()
def get_total_count(doc,depts,title):
    no_of_days = date_diff(add_days(doc.to_date, 1), doc.from_date)
    dates = [add_days(doc.from_date, i) for i in range(0, no_of_days)]
    data = '<td style="background-color:#27ae60">%s</td>'%title
    sales_amount = '<td style="background-color:#d4efdf">Sales Amount</td>'
    per_head = '<td style="background-color:#6495ED">Sales Per Head</td>'
    for date in dates:
        c = frappe.db.count("Attendance",{"attendance_date":date,'status':'Present',"Department":['in',depts]})
        data += '<td style="background-color:#27ae60">%s</td>'%c
        amt = frappe.db.get_value('Sales Amount Per Day', {
		'department': ['in', depts],
        'date': date
	}, 'sum(sales_amount)') or 0.0
        sales_amount += '<td style="background-color:#d4efdf">%s</td>'%amt
        try:
            ph_amt = round(amt/c,2)
        except:
            ph_amt = '-'
        per_head += '<td style="background-color:#6495ED">%s</td>'%ph_amt
    data = '<tr>' + data + '</tr><tr>' + sales_amount + '</tr><tr>' + per_head + '</tr>'
    return data

@frappe.whitelist()
def get_support_att_count(doc,depts,title):
    no_of_days = date_diff(add_days(doc.to_date, 1), doc.from_date)
    dates = [add_days(doc.from_date, i) for i in range(0, no_of_days)]
    data = '<td style="background-color:#27ae60">%s</td>'%title
    per_head = '<td style="background-color:#6495ED">Sales Per Head</td>'
    for date in dates:
        c = frappe.db.count("Attendance",{"attendance_date":date,'status':'Present',"Department":['in',depts]})
        data += '<td style="background-color:#27ae60">%s</td>'%c
        
    data = '<tr>' + data + '</tr>'
    return data

@frappe.whitelist()
def get_grand_total(doc,depts,title):
    no_of_days = date_diff(add_days(doc.to_date, 1), doc.from_date)
    dates = [add_days(doc.from_date, i) for i in range(0, no_of_days)]
    data = '<td style="background-color:#27ae60">%s</td>'%title
    sales_amount = '<td style="background-color:#d4efdf">Sales Amount</td>'
    per_head = '<td style="background-color:#6495ED">Sales Per Head</td>'
    for date in dates:
        c = frappe.db.count("Attendance",{"attendance_date":date,'status':'Present',"Department":['in',depts]})
        data += '<td style="background-color:#27ae60">%s</td>'%c
        amt = frappe.db.get_value('Sales Amount Per Day', {
		'department': ['in', depts],
        'date': date
	}, 'sum(sales_amount)') or 0.0
        sales_amount += '<td style="background-color:#d4efdf">%s</td>'%amt
        try:
            ph_amt = round(amt/c,2)
        except:
            ph_amt = '-'
        per_head += '<td style="background-color:#6495ED">%s</td>'%ph_amt
    data = '<tr>' + data + '</tr><tr>' + sales_amount + '</tr><tr>' + per_head + '</tr>'
    return data

day_abbr = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun"
]