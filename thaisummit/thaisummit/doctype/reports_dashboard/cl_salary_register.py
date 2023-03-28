from __future__ import unicode_literals
from os import stat
import frappe
from frappe.utils import cstr, add_days, date_diff, getdate, touch_file
from frappe import _
from frappe.utils.csvutils import UnicodeWriter, build_csv_response, read_csv_content
from frappe.utils.file_manager import get_file
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue
import openpyxl
from openpyxl import Workbook
import re
from openpyxl.styles import Font, Alignment,Border,Side
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import GradientFill, PatternFill
from six import BytesIO, string_types
from frappe.utils import  formatdate
from frappe import _, bold
from calendar import month, monthrange
from datetime import date, timedelta, datetime,time
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date

@frappe.whitelist()
def download():
    filename = 'CL Salary Register'
    test = build_xlsx_response(filename)

def make_xlsx(data, sheet_name=None, wb=None, column_widths=None):
    args = frappe.local.form_dict
    column_widths = column_widths or []
    if wb is None:
        wb = openpyxl.Workbook()
    ws = wb.create_sheet(sheet_name, 0)

    header_date = title (args)
    ws.append(header_date)

    header_date = title1(args)
    ws.append(header_date)

    header = add_header(args)
    ws.append(header)

    header_column = get_column(args)
    ws.append(header_column)
    
    data = get_data(args)
    for row in data:
        ws.append(row)

    align_center = Alignment(horizontal='center',vertical='center')
    for cell in ws["2:2"]:
        cell.alignment = align_center
        cell.font = Font(bold=True)
    for cell in ws['1:1']:
        cell.alignment = align_center
        cell.font = Font(bold=True)
    for cell in ws['3:3']:
        cell.alignment = align_center
        cell.font = Font(bold=True)

    border = Border(left=Side(border_style='thin'),
             right=Side(border_style='thin'),
             top=Side(border_style='thin'),
             bottom=Side(border_style='thin'))

    for rows in ws.iter_rows(min_row=1, max_row=len(get_data(args))+4, min_col=1, max_col=len(add_header(args))):
        for cell in rows:
            cell.border = border  

    ws.merge_cells(start_row=1, start_column=1, end_row=3, end_column= 6)
    ws.merge_cells(start_row=1, start_column=7, end_row=1, end_column= len(add_header(args)))
    ws.merge_cells(start_row=1, start_column=len(add_header(args))+1, end_row=1, end_column=len(add_header(args))+5)
    # ws.merge_cells(start_row=1, start_column=25, end_row=1, end_column= 33)

    for header in ws.iter_rows(min_row=1, max_row=3, min_col=1, max_col=len(get_column(args))):
            for cell in header:
                cell.fill = PatternFill(fgColor='92d14f', fill_type = "solid")
                cell.alignment = align_center
    for header in ws.iter_rows(min_row=4, max_row=4, min_col=1, max_col=6):
            for cell in header:
                cell.fill = PatternFill(fgColor='feedcc', fill_type = "solid",)
                cell.font = Font(bold=True)
                cell.alignment = align_center
    for header in ws.iter_rows(min_row=1, max_row=4, min_col=7, max_col=len(get_column(args))):
            for cell in header:
                cell.fill = PatternFill(fgColor='f3af84', fill_type = "solid")
                cell.font = Font(bold=True)
                cell.alignment = align_center
    
    ws.freeze_panes = 'G5'

    ws.sheet_view.zoomScale = 100 

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
def title(args):
    month = datetime.strptime(str(args.to_date),'%Y-%m-%d')
    mon = str(month.strftime('%B') +''+ str(month.strftime('%Y')))
    data = ["CL WAGE - "+mon,"",
            "",
            "",
            "",
            "",'Attendance']
    return data

@frappe.whitelist()
def title1(args):
    data = ["",
            "",
            "",
            "",
            "",
            "",'Type']
    dates = get_dates(args)
    for date in dates:
        holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
        left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where  holiday_date = '%s' """%(date),as_dict=True)
        status = ''
        if holiday :
            if holiday[0].weekly_off == 1:
                status = "WW"     
            else:
                status = "HH"
        else:
            status = "W"
        data.extend([status])
    return data

def get_dates(args):
    no_of_days = date_diff(add_days(args.to_date, 1), args.from_date)
    dates = [add_days(args.from_date, i) for i in range(0, no_of_days)]
    return dates  

@frappe.whitelist()
def get_column(args):
    data = []
    data += ['S No','Contractor',"ID","Name","Category","DOJ","Department/Day"]
    dates = get_dates(args)
    for date in dates:
        date = datetime.strptime(date,'%Y-%m-%d')
        day = datetime.date(date).strftime('%a')
        data.extend([day])
    return data  

@frappe.whitelist()
def add_header(args):
    header = ["","","","","","","Date"]
    dates = get_dates(args)
    for date in dates:
        date = datetime.strptime(date,'%Y-%m-%d')
        date = date.strftime('%d')
        header.extend([date])
    return header

@frappe.whitelist()
def add_day_header(args):
    day_header = ["","","","","","",""]
    dates = get_dates(args)
    for date in dates:
        date = datetime.strptime(date,'%Y-%m-%d')
        day = datetime.date(date).strftime('%a')
        day_header.extend([day])
    return day_header

def get_dates(args):
    no_of_days = date_diff(add_days(args['to_date'], 1), args['from_date'])
    dates = [add_days(args['from_date'], i) for i in range(0, no_of_days)]
    return dates

@frappe.whitelist() 
def get_data(args):
    data = []
    row = []
    basic_component_amount = earning_component_amount = deduction_component_amount = gross_wage = total_deduction = 0

    earning_comp = ["Basic","House Rent Allowance","Welding Allowance","Attendance Bonus","Additional Allowance","Shift Allowance","Arrear","PP Allowance","Transport Allowance","Others",]

    dedcution_comp = ["Provident Fund","Employee State Insurance","Canteen Charges","Professional Tax","Labor Welfare Fund","Tel EXP","Personal Protective Equipment","Advance" ]

    # if args.department:
    #     salary_slips = frappe.get_all("Salary Slip",{'employee_type':'BC''start_date':args.from_date,'end_date':args.to_date},['*'])	

    if args.employee:
        salary_slips = frappe.get_all("Salary Slip",{'employee_type':'CL','employee':args.employee,'start_date':args.from_date,'end_date':args.to_date},['*'])	
    
    else:
        salary_slips = frappe.get_all("Salary Slip",{'employee_type':'CL','start_date':args.from_date,'end_date':args.to_date},['*'])	
    i =1
    for ss in salary_slips:
        row = [i,]
        cost_center = frappe.get_value('Department',ss.department,'cost_centre')
        emp = frappe.get_doc("Employee",ss.employee)
        row += [emp.contractor,emp.name,emp.employee_name,emp.designation,formatdate(emp.date_of_joining),emp.department]
        dates = get_dates(args)
        for date in dates:
            att = frappe.db.get_value("Attendance",{'attendance_date':date,'employee':emp.name},['shift_status']) or '-'
            if att[0]:
                row.append(att[0])
            else:
                row.append('-')
        data.append(row)    
        # for ec in earning_comp:
        #     earning_component_amount = frappe.get_value('Salary Detail',{'salary_component':ec,'parent':ss.name},['amount'])
        #     if earning_component_amount:
        #         row.append(earning_component_amount)
        #     else:
        #         row.append('-')
        # row += [ss.gross_pay]
        # total_deduction =0
        # for dc in dedcution_comp:
        #     deduction_component_amount = frappe.get_value('Salary Detail',{'salary_component':dc,'parent':ss.name},['amount'])
        #     if deduction_component_amount:
        #         row += [deduction_component_amount]
        #         total_deduction += deduction_component_amount
        #     else:
        #         row += ['-']
        #     bonus_value = frappe.get_value('Salary Detail',{'salary_component':'Basic','parent':ss.name},['amount']) or 0
        #     bonus = round(bonus_value/12)

        # row.append(ss.total_deduction)
        # row += [ ss.net_pay ]
        # row += [ bonus ]
        # data.append(row)
        i+=1
        
    return data



              
