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
	data = 'hii'
	frappe.errprint(type(doc.from_date))
	# from_date = datetime.strptime(str(doc.from_date), "%Y-%m-%d")   # start date
    # to_date = datetime.strptime(str(doc.to_date),  "%Y-%m-%d")       # end date
	# frappe.errprint(from_date)
    # delta = doc.to_date - doc.from_date
	# frappe.errprint(delta)
    # for i in range(delta.days + 1):
    #     day = from_date + timedelta(days=i)
    #     day_name = day_abbr[getdate(day).weekday()]
    #     days += '<td>%s-%s</td>'%s(cstr(day.day),day_name)
	# no_of_days = date_diff(add_days(doc.to_date, 1), doc.from_date)
	# dates = [add_days(doc.from_date, i) for i in range(0, no_of_days)]
	# data = "<tr>"
	# for date in dates:
	# 	d = datetime.strptime(date, '%Y-%m-%d').date().strftime("%d-%b")
	# 	frappe.errprint(d)
	# 	data += "<td>%s</td>"%d
	# data += '</tr>'
	# days = ''
	# data = '<tr>' + days + '</tr>'
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