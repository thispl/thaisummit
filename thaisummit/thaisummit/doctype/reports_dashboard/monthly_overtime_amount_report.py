from __future__ import unicode_literals
from os import stat
import frappe
from frappe.utils import cstr, add_days, date_diff, getdate, touch_file
from frappe import _
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from frappe.utils.file_manager import get_file
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue

from datetime import date, timedelta, datetime, time

import openpyxl
from openpyxl import Workbook
import re
from openpyxl.styles import Font, Alignment,Border,Side
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import GradientFill, PatternFill
from six import BytesIO, string_types



@frappe.whitelist()
def download():
    filename = 'monthly ot amount report'
    test = build_xlsx_response(filename)


ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
# return xlsx file object
def make_xlsx(data, sheet_name=None, wb=None, column_widths=None):
    args = frappe.local.form_dict
    column_widths = column_widths or []
    if wb is None:
        wb = openpyxl.Workbook()

    ws = wb.create_sheet(sheet_name, 0)
    header_date = add_date(args)   
    ws.append(header_date)
    header_day = add_day(args)
    ws.append(header_day)
   
    data = get_data(args)

    for row in data:
        ws.append(row)
    
    dates = get_dates(args)

    align_center = Alignment(horizontal='center',vertical='center')
    for cell in ws["2:2"]:
        cell.alignment = align_center
        cell.fill = PatternFill(fgColor="ffff00", fill_type = "solid")
        
    align_center = Alignment(horizontal='center',vertical='center')
    for cell in ws["2:2"]:
        cell.alignment = align_center
        cell.font = Font(bold=True)
    for cell in ws['1:1']:
        cell.alignment = align_center
        cell.font = Font(bold=True)
    for cell in ws['A:A']:
        cell.alignment = align_center
        cell.font = Font(bold=True)
    
   

    iym = frappe.db.count('Department',{'parent_department':'IYM','is_group':0})
    re = frappe.db.count('Department',{'parent_department':'RE','is_group':0})
    ford = frappe.db.count('Department',{'parent_department':'FORD','is_group':0})
    support = frappe.db.count('Department',{'parent_department':'SUPPORT','is_group':0})
    departments = (iym+re+ford+support)

    border = Border(left=Side(border_style='thin', color='000000'),
             right=Side(border_style='thin', color='000000'),
             top=Side(border_style='thin', color='000000'),
             bottom=Side(border_style='thin', color='000000'))
    for rows in ws.iter_rows(min_row=1, max_row=departments+18, min_col=1, max_col=len(dates)+3):
        for cell in rows:
            cell.border = border


    ws.merge_cells(start_row=3, start_column=1, end_row=iym+5, end_column=1)
    ws.merge_cells(start_row=iym+6, start_column=1, end_row=iym+8+re, end_column=1)
    ws.merge_cells(start_row=iym+9+re, start_column=1, end_row=iym+11+ford+re, end_column=1)
    ws.merge_cells(start_row=iym+12+ford+re, start_column=1, end_row=iym+14+ford+re, end_column=1)
    ws.merge_cells(start_row=iym+15+ford+re, start_column=1, end_row=iym+14+ford+re+support, end_column=1)
    ws.merge_cells(start_row=iym+15+ford+re+support, start_column=1, end_row=iym+18+ford+re+support, end_column=1)

    

    ws.merge_cells(start_row=1, start_column=1, end_row=2, end_column= 1)
    ws.merge_cells(start_row=1, start_column=len(dates)+3, end_row=2, end_column= len(dates)+3)



    for dept_name in ws.iter_rows(min_row=3, max_row=iym+2, min_col=2, max_col=2):
            for cell in dept_name:
                cell.fill = PatternFill(fgColor='ffff00', fill_type = "solid")

    for dept_name in ws.iter_rows(min_row=iym+2, max_row=iym+re+5, min_col=2, max_col=2):
            for cell in dept_name:
                cell.fill = PatternFill(fgColor='ffff00', fill_type = "solid")
    for dept_name in ws.iter_rows(min_row=iym+re+3, max_row=iym+8+re+ford, min_col=2, max_col=2):
            for cell in dept_name:
                cell.fill = PatternFill(fgColor='ffff00', fill_type = "solid")
    for dept_name in ws.iter_rows(min_row=iym+re+ford+3, max_row=iym+14+re+ford+support, min_col=2, max_col=2):
            for cell in dept_name:
                cell.fill = PatternFill(fgColor='ffff00', fill_type = "solid")
    
    


    for rows in ws.iter_rows(min_row=iym+3, max_row=iym+3, min_col=2, max_col=len(dates)+3):
        for cell in rows:
            cell.fill = PatternFill(fgColor='8ECA50', fill_type = "solid")
            cell.font = Font(bold=True)

    for rows in ws.iter_rows(min_row=iym+6+re, max_row=iym+6+re, min_col=2, max_col=len(dates)+3):
        for cell in rows:
            cell.fill = PatternFill(fgColor='8ECA50', fill_type = "solid")
            cell.font = Font(bold=True)
    
    for rows in ws.iter_rows(min_row=iym+9+re+ford, max_row=iym+9+re+ford, min_col=2, max_col=len(dates)+3):
        for cell in rows:
            cell.fill = PatternFill(fgColor='8ECA50', fill_type = "solid")
            cell.font = Font(bold=True)
        
    for rows in ws.iter_rows(min_row=iym+12+re+ford, max_row=iym+12+re+ford, min_col=2, max_col=len(dates)+3):
        for cell in rows:
            cell.fill = PatternFill(fgColor='8ECA50', fill_type = "solid")
            cell.font = Font(bold=True)

    for rows in ws.iter_rows(min_row=iym+15+re+ford+support, max_row=iym+15+re+ford+support, min_col=2, max_col=len(dates)+3):
        for cell in rows:
            cell.fill = PatternFill(fgColor='8ECA50', fill_type = "solid")
            cell.font = Font(bold=True)
    
    
    for rows in ws.iter_rows(min_row=iym+4, max_row=iym+4, min_col=2, max_col=len(dates)+3):
        for cell in rows:
            cell.fill = PatternFill(fgColor='D0D5CC', fill_type = "solid")
            cell.font = Font(bold=True)

    for rows in ws.iter_rows(min_row=iym+7+re, max_row=iym+7+re, min_col=2, max_col=len(dates)+3):
        for cell in rows:
            cell.fill = PatternFill(fgColor='D0D5CC', fill_type = "solid")
            cell.font = Font(bold=True)
    
    for rows in ws.iter_rows(min_row=iym+10+re+ford, max_row=iym+10+re+ford, min_col=2, max_col=len(dates)+3):
        for cell in rows:
            cell.fill = PatternFill(fgColor='D0D5CC', fill_type = "solid")
            cell.font = Font(bold=True)
        
    for rows in ws.iter_rows(min_row=iym+13+re+ford, max_row=iym+13+re+ford, min_col=2, max_col=len(dates)+3):
        for cell in rows:
            cell.fill = PatternFill(fgColor='D0D5CC', fill_type = "solid")
            cell.font = Font(bold=True)

    for rows in ws.iter_rows(min_row=iym+17+re+ford+support, max_row=iym+17+re+ford+support, min_col=2, max_col=len(dates)+3):
        for cell in rows:
            cell.fill = PatternFill(fgColor='D0D5CC', fill_type = "solid")
            cell.font = Font(bold=True)
    for total in ws.iter_rows(min_row=iym+16+re+ford+support, max_row=iym+16+re+ford+support, min_col=2, max_col=len(dates)+3):
        for cell in total:
            cell.fill = PatternFill(fgColor='4A934E', fill_type = "solid")
            cell.font = Font(bold=True)

    
    for rows in ws.iter_rows(min_row=iym+5, max_row=iym+5, min_col=2, max_col=len(dates)+3):
        for cell in rows:
            cell.fill = PatternFill(fgColor='46A1E9', fill_type = "solid")
            cell.font = Font(bold=True)

    for rows in ws.iter_rows(min_row=iym+8+re, max_row=iym+8+re, min_col=2, max_col=len(dates)+3):
        for cell in rows:
            cell.fill = PatternFill(fgColor='46A1E9', fill_type = "solid")
            cell.font = Font(bold=True)
    
    for rows in ws.iter_rows(min_row=iym+11+re+ford, max_row=iym+11+re+ford, min_col=2, max_col=len(dates)+3):
        for cell in rows:
            cell.fill = PatternFill(fgColor='46A1E9', fill_type = "solid")
            cell.font = Font(bold=True)
        
    for rows in ws.iter_rows(min_row=iym+14+re+ford, max_row=iym+14+re+ford, min_col=2, max_col=len(dates)+3):
        for cell in rows:
            cell.fill = PatternFill(fgColor='46A1E9', fill_type = "solid")
            cell.font = Font(bold=True)

    for rows in ws.iter_rows(min_row=iym+18+re+ford+support, max_row=iym+18+re+ford+support, min_col=2, max_col=len(dates)+3):
        for cell in rows:
            cell.fill = PatternFill(fgColor='46A1E9', fill_type = "solid")
            cell.font = Font(bold=True)
    
    
    ws.freeze_panes='C3'
    ws.sheet_view.zoomScale = 80 

    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    return xlsx_file

def build_xlsx_response(filename):
    xlsx_file = make_xlsx(filename)
    # write out response as a xlsx type
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type'] = 'binary'


@frappe.whitelist()
def add_day(args):
    data = ['',"Day",]
    no_of_days = date_diff(add_days(args.to_date, 1), args.from_date)
    dates = [add_days(args.from_date, i) for i in range(0, no_of_days)]
    for date in dates:
        dt = datetime.strptime(date,'%Y-%m-%d')
        day_format = datetime.date(dt).strftime('%a')
        data.append(day_format)
    return data
    
@frappe.whitelist()
def add_date(args):
    data = ['#',"Date",]
    no_of_days = date_diff(add_days(args.to_date, 1), args.from_date)
    dates = [add_days(args.from_date, i) for i in range(0, no_of_days)]
    for date in dates:
        dt = datetime.strptime(date,'%Y-%m-%d')
        day_format = datetime.date(dt).strftime('%d-%m')
        data.append(day_format)
    data.append("Actual Amt")
    return data

@frappe.whitelist()
def get_data(args):
    data = []
    dept_group = ['IYM','RE','FORD',]
    mfg_dept_list = []
    mfg_ot_amt_header = ['MFG','OT Amount']
    mfg_ot_percent_header=['','OT%']
    mfg_ot_sales_amt = ['',"Sales Amount"]
      
    for dg in dept_group:
        ot_amt_header = ['','OT Amount']
        ot_percent_header = ['','OT%']
        ot_sales_amt = ['',"Sales Amount"]
        departments = frappe.get_all("Department",{'parent_department':dg,"is_group":"0"},)
        dept_list = []
        for dept in departments:
            dept_list.append(dept.name)
            mfg_dept_list.append(dept.name)
        for dept in departments:
            row = [dg,dept.name]
            dates = get_dates(args)
            total_ot_amt = 0
            for date in dates:
                t_ot = 0
                ot_amt = 0
                ot_hrs = timedelta(0,0,0)
                ots = frappe.get_all("Overtime Request",{"department":dept.name,"ot_date":date,"workflow_state":"Approved"},["employee","ot_hours"])
                for ot in ots:
                    ot_hrs = ot.ot_hours
                    amt_per_hr = ((frappe.db.get_value("Employee",ot.employee,'basic')/26)/8)*2
                    day = ot_hrs.days * 24
                    hours = day + ot_hrs.seconds // 3600
                    minutes = (ot_hrs.seconds//60)%60
                    ftr = [3600,60,1]
                    hr = (sum([a*b for a,b in zip(ftr, map(int,str(str(hours) +':'+str(minutes)+':00').split(':')))]))/3600
                    ot_amt = hr * amt_per_hr
                    t_ot += ot_amt
                    total_ot_amt += ot_amt
                row.append(t_ot)
            row.append(total_ot_amt)
                
            data.append(row)
        dates = get_dates(args)
        total_ot_amt = 0
        for date in dates:
            t_ot = 0
            ot_hrs = timedelta(0,0,0)
            ots = frappe.get_all("Overtime Request",{"department":('in',(dept_list)),"ot_date":date,"workflow_state":"Approved"},["employee","ot_hours"])
            for ot in ots:
                ot_hrs = ot.ot_hours
                amt_per_hr = ((frappe.db.get_value("Employee",ot.employee,'basic')/26)/8)*2
                day = ot_hrs.days * 24
                hours = day + ot_hrs.seconds // 3600
                minutes = (ot_hrs.seconds//60)%60
                ftr = [3600,60,1]
                hr = (sum([a*b for a,b in zip(ftr, map(int,str(str(hours) +':'+str(minutes)+':00').split(':')))]))/3600
                ot_amt = hr * amt_per_hr
                t_ot += ot_amt
                total_ot_amt += ot_amt
            ot_amt_header.append(t_ot)
            ot_percent_header.append("0")
            ot_sales_amt.append("0")
        ot_amt_header.append(total_ot_amt)

        data.append(ot_amt_header)
        data.append(ot_sales_amt)
        data.append(ot_percent_header)
    total_mfg_ot_amt = 0
    for date in dates:
        mfg_t_ot = 0
        mfg_ot_hrs = timedelta(0,0,0)
        mfg_ot = frappe.get_all("Overtime Request",{"department":('in',(mfg_dept_list)),"ot_date":date,"workflow_state":"Approved"},["employee","ot_hours"])
        for mf_ot in mfg_ot:
            mfg_ot_hrs = mf_ot.ot_hours
            day = mfg_ot_hrs.days * 24
            hours = day + mfg_ot_hrs.seconds // 3600
            minutes = (mfg_ot_hrs.seconds//60)%60
            ftr = [3600,60,1]
            hr = (sum([a*b for a,b in zip(ftr, map(int,str(str(hours) +':'+str(minutes)+':00').split(':')))]))/3600
            amt_per_hr = ((frappe.db.get_value("Employee",ot.employee,'basic')/26)/8)*2
            mfg_ot_amt = hr * amt_per_hr
            mfg_t_ot += mfg_ot_amt
            total_mfg_ot_amt += mfg_ot_amt
        mfg_ot_amt_header.append(mfg_t_ot)
        mfg_ot_percent_header.append("0")
        mfg_ot_sales_amt.append("0")
    mfg_ot_amt_header.append(total_mfg_ot_amt)
    # mfg_ot_percent_header.append("0")
    # mfg_ot_sales_amt.append("0")

    data.append(mfg_ot_amt_header)
    data.append(mfg_ot_sales_amt)
    data.append(mfg_ot_percent_header)
    support = get_support(args)
    
    for s in support:
        data.append(s)
    tsai = get_tsai(args)
    for ts in tsai:
        data.append(ts)

    return data
    
def get_dates(args):
    no_of_days = date_diff(add_days(args.to_date, 1), args.from_date)
    dates = [add_days(args.from_date, i) for i in range(0, no_of_days)]
    return dates

def get_support(args):
    departments = frappe.get_all("Department",{'parent_department':'SUPPORT',"is_group":"0"},)
    support_data = []
    support_dept_list = []
   
    for dept in departments:
        row = ['SUPPORT',dept.name]
        dates = get_dates(args)
        support_dept_list.append(dept.name)
        total_ot_amt =0
        for date in dates:
            t_ot = 0
            ot_hrs = timedelta(0,0,0)
            ots = frappe.get_all("Overtime Request",{"department":dept.name,"ot_date":date,"workflow_state":"Approved"},["employee","ot_hours"])
            for ot in ots:
                ot_hrs = ot.ot_hours
                day = ot_hrs.days * 24
                hours = day + ot_hrs.seconds // 3600
                minutes = (ot_hrs.seconds//60)%60
                ftr = [3600,60,1]
                hr = (sum([a*b for a,b in zip(ftr, map(int,str(str(hours) +':'+str(minutes)+':00').split(':')))]))/3600
                amt_per_hr = ((frappe.db.get_value("Employee",ot.employee,'basic')/26)/8)*2
                ot_amt = hr * amt_per_hr
                t_ot += ot_amt
                total_ot_amt+=ot_amt
            row.append(t_ot)
            # row.append(total_ot_amt)
        row.append(total_ot_amt)
        support_data.append(row)
    return support_data

def get_tsai(args):
    data = []
    dates = get_dates(args)
    tsai_ot_amount_header = ['TSAI','OT Amount']
    tsai_sales_amount_header = ['','Sales Amount']
    tsai_ot_percent_header = ['','OT %']
    dept_list = []
    departments = frappe.get_all("Department",{'parent_department':'SUPPORT',"is_group":"0"},)
    for dept in departments:
        dept_list.append(dept.name)
    actual_ot_amt = 0
    for date in dates:
        total_ot_amt = 0
        ot_hrs = timedelta(0,0,0)
        mfg_ot = frappe.get_all("Overtime Request",{"department":('in',(dept_list)),"ot_date":date,"workflow_state":"Approved"},["employee","ot_hours"])
        for ot in mfg_ot:
            ot_hrs = ot.ot_hours
            day = ot_hrs.days * 24
            hours = day + ot_hrs.seconds // 3600
            minutes = (ot_hrs.seconds//60)%60
            ftr = [3600,60,1]
            hr = (sum([a*b for a,b in zip(ftr, map(int,str(str(hours) +':'+str(minutes)+':00').split(':')))]))/3600
            amt_per_hr = ((frappe.db.get_value("Employee",ot.employee,'basic')/26)/8)*2
            ot_amt = hr * amt_per_hr
            # t_ot += ot_amt
            total_ot_amt += ot_amt
            actual_ot_amt+=total_ot_amt
        tsai_ot_amount_header.append(total_ot_amt)
        tsai_sales_amount_header.append('0')
        tsai_ot_percent_header.append('0')
    tsai_ot_amount_header.append(actual_ot_amt)
    data.append(tsai_ot_amount_header)
    g_total = grand_total(args)
    for g in g_total:
        data.append(g)
    data.append(tsai_sales_amount_header)
    data.append(tsai_ot_percent_header)
    return data
# def grand_total(args,get_data,get_tsai):
#     data = []
#     grand_total_header = ['']
#     dates = get_dates(args)
#     for date in dates:
#         grand_total = get_data.total_mfg_ot_amt +  get_tsai.total_ot_amt
#         grand_total_header.append(grand_total)
#     data.append(grand_total_header)
#     return data
def grand_total(args):
    data = []
    dept_group = ['IYM','RE','FORD','SUPPORT']
    grand_total_header = ['','Grand Total']
    dept_list = []
    for dg in dept_group:
        departments = frappe.get_all("Department",{'parent_department':dg,"is_group":"0"},)  
        for dept in departments:
            dept_list.append(dept.name)
    dates = get_dates(args)
    actual_ot_amt=0
    for date in dates:
        ot_hrs = timedelta(0,0,0)
        total_ot_amt = 0
        ots = frappe.get_all("Overtime Request",{"department":('in',(dept_list)),"ot_date":date,"workflow_state":"Approved"},["ot_hours"])
        for ot in ots:
            ot_hrs += ot.ot_hours
        day = ot_hrs.days * 24
        hours = day + ot_hrs.seconds // 3600
        minutes = (ot_hrs.seconds//60)%60
        ftr = [3600,60,1]
        hr = (sum([a*b for a,b in zip(ftr, map(int,str(str(hours) +':'+str(minutes)+':00').split(':')))]))/3600
        ot_amt = hr * 50
        total_ot_amt += ot_amt
        actual_ot_amt+=total_ot_amt
        grand_total_header.append(total_ot_amt)
    grand_total_header.append(actual_ot_amt)
    data.append(grand_total_header)
    return data
            








    









    