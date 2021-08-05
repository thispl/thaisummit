# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from inspect import ArgSpec
from babel import dates
import frappe
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
from frappe import _, bold
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from frappe.utils.data import format_date
from frappe.utils.file_manager import get_file
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue

from datetime import date, timedelta, datetime
import openpyxl
from openpyxl import Workbook


import openpyxl
from requests.api import head
from thaisummit.custom import get_dates
import xlrd
import re
from openpyxl.styles import Font, Alignment
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import GradientFill, PatternFill
from six import BytesIO, string_types

class ShiftScheduleSummaryReport(Document):
    pass


@frappe.whitelist()
def download():
    filename = 'Monthly Manpower Report'
    test = build_xlsx_response(filename)


# return xlsx file object
def make_xlsx(data, sheet_name=None, wb=None, column_widths=None):
    args = frappe.local.form_dict
    column_widths = column_widths or []
    if wb is None:
        wb = openpyxl.Workbook()

    ws = wb.create_sheet(sheet_name, 0)

    report_title = ['Monthly Manpower Report']
    ws.append(report_title)

    header = add_header(args)
    ws.append(header)

    header = add_day_header(args)
    ws.append(header)

    header = add_header_emp_type(args)
    ws.append(header)

    data = get_data(args)

    for row in data:
        ws.append(row)

    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=10)

    dates = get_dates(args)
    i = 2
    for n in range(len(dates)):
        j = i + 5
        ws.merge_cells(start_row=2, start_column=i, end_row=2, end_column=j)
        ws.merge_cells(start_row=3, start_column=i, end_row=3, end_column=j)
        ws.cell(row=2,column=i).alignment = Alignment(horizontal='center')
        ws.cell(row=3,column=i).alignment = Alignment(horizontal='center')
        i += 6


    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    return xlsx_file    


def build_xlsx_response(filename):
    xlsx_file = make_xlsx(filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type'] = 'binary'


@frappe.whitelist()
def add_header(args):
    header = ["Date"]
    dates = get_dates(args)
    for date in dates:
        header.extend([date,'','','','',''])
    return header

@frappe.whitelist()
def add_day_header(args):
    day_header = ["Day"]
    dates = get_dates(args)
    for date in dates:
        day_header.extend([date,'','','','',''])
    return day_header

@frappe.whitelist()
def add_header_emp_type(args):
    header = ["DEPT"]
    emp_type = ['WC','BC','FT','NT','CL','TT']
    dates = get_dates(args)
    for i in range(len(dates)):
        header.extend(emp_type)
    return header

def get_dates(args):
    no_of_days = date_diff(add_days(args.to_date, 1), args.from_date)
    dates = [add_days(args.from_date, i) for i in range(0, no_of_days)]
    return dates

def get_data(args):
    data = []
    dept_group = ['IYM','RE','FORD','SUPPORT']
    for dg in dept_group:
        # for i in range(2):
        departments = frappe.get_all('Department',{'parent_department':dg,'is_group':0,'direct':1})
        dept_list = []
        for dp in departments:
            dept_list.append(dp.name)
        for dept in departments:
            row = [dept.name]
            dates = get_dates(args)
            employee_type = ['WC','BC','FT','NT','CL','TT']
            for date in dates:
                total_count = 0
                wc_count = 0
                for emp_type in employee_type:
                    if emp_type == 'WC':
                        count = frappe.db.sql("select count(*) as count from `tabAttendance` where attendance_date = '%s' and status in ('Present','Half Day') and docstatus != 2 and employee_type = 'WC' and department = '%s' "%(date,dept.name),as_dict=True)
                        if count:
                            wc_count = count[0].count
                        else:
                            wc_count = 0
                        row.append(wc_count)
                    elif emp_type != 'TT':
                        count = frappe.db.count("QR Checkin",{'department':dept.name,'shift_date':date,'employee_type':emp_type,'ot':0})
                        row.append(count)
                        total_count += count
                    else:
                        row.append(total_count + wc_count)
        row = ['Total Direct' + dept.name]
        dates = get_dates(args)
        employee_type = ['WC','BC','FT','NT','CL','TT']
        depts = str(dept_list).replace('[','(')
        depts = str(depts).replace(']',')')
        for date in dates:
            total_count = 0
            wc_count = 0
            for emp_type in employee_type:
                if emp_type == 'WC':
                    query = """select count(*) as count from `tabAttendance` where attendance_date = '%s' and status in ('Present','Half Day') and docstatus != 2 and employee_type = 'WC' and department in "%s" """%(date,tuple(dept_list))
                    frappe.errprint(query)
                    frappe.log_error(message=query,title='count')
                    count = frappe.db.sql(query,as_dict=True)
                    if count:
                        wc_count = count[0].count
                    else:
                        wc_count = 0
                    row.append(wc_count)
                elif emp_type != 'TT':
                    count = frappe.db.count("QR Checkin",{'department':('in',tuple(dept_list)),'shift_date':date,'employee_type':emp_type,'ot':0})
                    row.append(count)
                    total_count += count
                else:
                    row.append(total_count + wc_count)

#             for contractor in contractors:
#                 shifts = ['1','2','3','PP2','TT']
#                 total_count = 0
#                 for shift in shifts:
#                     if shift != 'TT':
#                         count = frappe.db.sql("select count(*) as count from `tabShift Assignment` left join `tabEmployee` on `tabShift Assignment`.employee = `tabEmployee`.name where `tabEmployee`.contractor = '%s' and `tabShift Assignment`.shift_type = '%s' and `tabShift Assignment`.start_date = '%s' and `tabShift Assignment`.employee_type = 'CL' and `tabShift Assignment`.department = '%s' "%(contractor.name,shift,args.date,dept.name),as_dict=True)
#                         if count:
#                             count = count[0].count
#                         else:
#                             count = 0
#                         row.append(count)
#                         total_count += count
#                     else:
#                         row.append(total_count)
#             total_count = 0
#             for shift in shifts:
#                 if shift != 'TT':
#                     count = frappe.db.sql("select count(*) as count from `tabShift Assignment` left join `tabEmployee` on `tabShift Assignment`.employee = `tabEmployee`.name where `tabShift Assignment`.shift_type = '%s' and `tabShift Assignment`.start_date = '%s' and `tabShift Assignment`.employee_type = 'CL' and `tabShift Assignment`.department = '%s' "%(shift,args.date,dept.name),as_dict=True)
#                     if count:
#                         count = count[0].count
#                     else:
#                         count = 0
#                     row.append(count)
#                     total_count += count
#                 else:
#                     row.append(total_count)
#             total_count = 0
#             for shift in shifts:
#                 if shift != 'TT':
#                     count = frappe.db.sql("select count(*) as count from `tabShift Assignment` left join `tabEmployee` on `tabShift Assignment`.employee = `tabEmployee`.name where `tabShift Assignment`.shift_type = '%s' and `tabShift Assignment`.start_date = '%s' and `tabShift Assignment`.employee_type = 'CL' and `tabShift Assignment`.department = '%s' and `tabEmployee`.vacant = 1 "%(shift,args.date,dept.name),as_dict=True)
#                     if count:
#                         count = count[0].count
#                     else:
#                         count = 0
#                     row.append(count)
#                     total_count += count
#                 else:
#                     row.append(total_count)
            data.append(row)

#         row = [dg,'TOTAL ' + dg]
#         shifts = ['1','2','3','PP2','TOTAL']
#         employee_type = ['WC','BC','FT','NT','CL','TT']
#         for shift in shifts:
#             if shift != 'TOTAL':
#                 total_count = 0
#                 for emp_type in employee_type:
#                     if emp_type != 'TT':
#                         count = frappe.db.count("Shift Assignment",{'department':('in',dept_list),'start_date':args.date,'shift_type':shift,'employee_type':emp_type,'docstatus':'1'})
#                         total_count += count
#                         row.append(count)
#                     else:
#                         row.append(total_count)
#             else:
#                 total_count = 0
#                 for emp_type in employee_type:
#                     if emp_type != 'TT':
#                         count = frappe.db.count("Shift Assignment",{'department':('in',dept_list),'start_date':args.date,'employee_type':emp_type,'docstatus':'1'})
#                         total_count += count
#                         row.append(count)
#                     else:
#                         row.append(total_count)
#         for contractor in contractors:
#                 shifts = ['1','2','3','PP2','TT']
#                 total_count = 0
#                 depts = str(dept_list).replace('[','(')
#                 depts = str(depts).replace(']',')')
#                 for shift in shifts:
#                     if shift != 'TT':
#                         count = frappe.db.sql("select count(*) as count from `tabShift Assignment` left join `tabEmployee` on `tabShift Assignment`.employee = `tabEmployee`.name where `tabEmployee`.contractor = '%s' and `tabShift Assignment`.shift_type = '%s' and `tabShift Assignment`.start_date = '%s' and `tabShift Assignment`.employee_type = 'CL' and `tabShift Assignment`.department in %s "%(contractor.name,shift,args.date,depts),as_dict=True)
#                         if count:
#                             count = count[0].count
#                         else:
#                             count = 0
#                         row.append(count)
#                         total_count += count
#                     else:
#                         row.append(total_count)
#         total_count = 0
#         for shift in shifts:
#             if shift != 'TT':
#                 count = frappe.db.sql("select count(*) as count from `tabShift Assignment` left join `tabEmployee` on `tabShift Assignment`.employee = `tabEmployee`.name where `tabShift Assignment`.shift_type = '%s' and `tabShift Assignment`.start_date = '%s' and `tabShift Assignment`.employee_type = 'CL' and `tabShift Assignment`.department in %s "%(shift,args.date,depts),as_dict=True)
#                 if count:
#                     count = count[0].count
#                 else:
#                     count = 0
#                 row.append(count)
#                 total_count += count
#             else:
#                 row.append(total_count)
#         total_count = 0
#         for shift in shifts:
#             if shift != 'TT':
#                 count = frappe.db.sql("select count(*) as count from `tabShift Assignment` left join `tabEmployee` on `tabShift Assignment`.employee = `tabEmployee`.name where `tabShift Assignment`.shift_type = '%s' and `tabShift Assignment`.start_date = '%s' and `tabShift Assignment`.employee_type = 'CL' and `tabShift Assignment`.department in %s and `tabEmployee`.vacant = 1 "%(shift,args.date,depts),as_dict=True)
#                 if count:
#                     count = count[0].count
#                 else:
#                     count = 0
#                 row.append(count)
#                 total_count += count
#             else:
#                 row.append(total_count)
#         data.append(row)

#     row = ['','TOTAL ']
#     shifts = ['1','2','3','PP2','TOTAL']
#     employee_type = ['WC','BC','FT','NT','CL','TT']
#     for shift in shifts:
#         if shift != 'TOTAL':
#             total_count = 0
#             for emp_type in employee_type:
#                 if emp_type != 'TT':
#                     count = frappe.db.count("Shift Assignment",{'start_date':args.date,'shift_type':shift,'employee_type':emp_type,'docstatus':'1'})
#                     total_count += count
#                     row.append(count)
#                 else:
#                     row.append(total_count)
#         else:
#             total_count = 0
#             for emp_type in employee_type:
#                 if emp_type != 'TT':
#                     count = frappe.db.count("Shift Assignment",{'start_date':args.date,'employee_type':emp_type,'docstatus':'1'})
#                     total_count += count
#                     row.append(count)
#                 else:
#                     row.append(total_count)
#     for contractor in contractors:
#         shifts = ['1','2','3','PP2','TT']
#         total_count = 0
#         for shift in shifts:
#             if shift != 'TT':
#                 count = frappe.db.sql("select count(*) as count from `tabShift Assignment` left join `tabEmployee` on `tabShift Assignment`.employee = `tabEmployee`.name where `tabEmployee`.contractor = '%s' and `tabShift Assignment`.shift_type = '%s' and `tabShift Assignment`.start_date = '%s' and `tabShift Assignment`.employee_type = 'CL' "%(contractor.name,shift,args.date),as_dict=True)
#                 if count:
#                     count = count[0].count
#                 else:
#                     count = 0
#                 row.append(count)
#                 total_count += count
#             else:
#                 row.append(total_count)
#     total_count = 0
#     for shift in shifts:
#         if shift != 'TT':
#             count = frappe.db.sql("select count(*) as count from `tabShift Assignment` left join `tabEmployee` on `tabShift Assignment`.employee = `tabEmployee`.name where `tabShift Assignment`.shift_type = '%s' and `tabShift Assignment`.start_date = '%s' and `tabShift Assignment`.employee_type = 'CL' "%(shift,args.date),as_dict=True)
#             if count:
#                 count = count[0].count
#             else:
#                 count = 0
#             row.append(count)
#             total_count += count
#         else:
#             row.append(total_count)
#     total_count = 0
#     for shift in shifts:
#         if shift != 'TT':
#             count = frappe.db.sql("select count(*) as count from `tabShift Assignment` left join `tabEmployee` on `tabShift Assignment`.employee = `tabEmployee`.name where `tabShift Assignment`.shift_type = '%s' and `tabShift Assignment`.start_date = '%s' and `tabShift Assignment`.employee_type = 'CL' and `tabEmployee`.vacant = 1 "%(shift,args.date),as_dict=True)
#             if count:
#                 count = count[0].count
#             else:
#                 count = 0
#             row.append(count)
#             total_count += count
#         else:
#             row.append(total_count)
#     data.append(row)
    return data
