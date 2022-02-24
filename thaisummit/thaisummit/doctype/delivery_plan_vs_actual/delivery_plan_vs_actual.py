# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
from email import message
from fileinput import filename
from os import stat
import frappe
from frappe.utils import cstr, add_days, date_diff,format_datetime
from frappe import _
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from frappe.utils.file_manager import get_file
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue

from datetime import date, timedelta, datetime, time

import openpyxl
from openpyxl import Workbook
import re
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import GradientFill, PatternFill
from six import BytesIO, string_types

class DeliveryPlanvsActual(Document):
    pass
@frappe.whitelist()
def download():
    filename = 'Delivery Plan vs Actual'
    test = build_xlsx_response(filename)


def make_xlsx(data, sheet_name=None, wb=None, column_widths=None):
    args = frappe.local.form_dict
    column_widths = column_widths or []
    if wb is None:
        wb = openpyxl.Workbook()

    ws = wb.create_sheet(sheet_name, 0)
    dates = get_dates(args)
    header = ["","",""]
    for d in dates:
        header.extend([d,"","",""])
    header.extend(["TOTAL","","",""])
    
    
        
    ws.append(header)
    
    header_title = ["MAT NO","PART NO","PART NAME"]
    for d in dates:
        header_title.extend(["PLAN","ACTUAL","DIFF","%"])
    header_title.extend(["PLAN","ACTUAL","DIFF","%"])

    ws.append(header_title)
    i = 4
    for d in dates:
        ws.merge_cells(start_row=1, start_column=i, end_row=1, end_column=i+3)
        i += 4
    # ws.merge_cells(start_row=1, start_column=8, end_row=1, end_column=12)
    # header3=["TOTAL","",""]
    # ws.append(header3)

    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    return xlsx_file


def build_xlsx_response(filename):
    xlsx_file = make_xlsx(filename)
    # write out response as a xlsx type
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type'] = 'binary'
    
def get_dates(args):
    no_of_days = date_diff(add_days(args.to_date, 1), args.from_date)
    dates = [add_days(args.from_date, i) for i in range(0, no_of_days)]
    return dates