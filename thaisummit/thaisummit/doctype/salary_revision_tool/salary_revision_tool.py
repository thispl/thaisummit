# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from codecs import ignore_errors
import re
import frappe
from frappe.model.document import Document
import openpyxl
from openpyxl import Workbook
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from frappe.utils import cstr, add_days, data, date_diff, getdate
from frappe.utils.file_manager import get_file
from six import BytesIO, string_types
from frappe.utils.background_jobs import enqueue

class SalaryRevisionTool(Document):
    @frappe.whitelist()
    def on_submit(self):
        # self.upload_salary()
        enqueue(self.upload_salary, queue='default', timeout=6000, event='upload_salary')

    @frappe.whitelist()
    def validate_file(self):
        file = get_file(self.file)
        pps = read_csv_content(file[1])
        err_list = ''
        for pp in pps:
            if pp[0] != 'Employee ID':
                if not frappe.db.exists('Employee',pp[0]):
                    err_list += "<ul>Employee <b>%s</b> not found.<br></ul>"%(pp[0])
        if err_list:
            self.file = ''
            return err_list

    @frappe.whitelist()
    def upload_salary(self):
        file = get_file(self.file)
        pps = read_csv_content(file[1])
        err_list = ''
        for pp in pps:
            if pp[0] != 'Employee ID':
                if not frappe.db.exists('Employee',pp[0]):
                    err_list += "<ul>Employee <b>%s</b> not found.<br></ul>"%(pp[0])
        if err_list:
            self.file = ''
            frappe.throw(err_list)
        else:
            for pp in pps:
                if pp[0] != 'Employee ID':
                    frappe.errprint(pp[0])
                    if pp[0]:
                        emp = frappe.new_doc('Salary Revision Entry')
                        emp.employee=pp[0]
                        emp.employee_name=pp[1]
                        emp.basic = pp[2]
                        emp.hra = pp[3]
                        emp.convey = pp[4]
                        emp.spl = pp[5]
                        emp.other = pp[6]
                        emp.ma = pp[7]
                        emp.leave_travel_allowance = pp[8]
                        emp.pos = pp[9]
                        emp.child = pp[10]
                        emp.hostel = pp[11]
                        emp.wash = pp[12]
                        emp.temp = pp[13]
                        emp.service = pp[14]
                        emp.ppe = pp[15]
                        emp.epf =pp[16]
                        emp.esi=pp[17]
                        emp.gross=pp[18]
                        emp.ctc=pp[19]
                        # if emp.basic != 0:
                        #     emp.append('salary_revision',{
                        #         'date' : self.date,
                        #         'basic' : emp.basic,
                        #         'house_rent_allowance':emp.house_rent_allowance,
                        #         'conveyance_allowance':emp.conveyance_allowance,
                        #         'special_allowance':emp.special_allowance,
                        #         'other_allowance':emp.other_allowance,
                        #         'medical_allowance':emp.medical_allowance,
                        #         'leave_travel_allowance':emp.leave_travel_allowance,
                        #         'position_allowance':emp.position_allowance,
                        #         'children_education':emp.children_education,
                        #         'children_hostel':emp.children_hostel,
                        #         'washing_allowance':emp.washing_allowance,
                        #         'welding_allowance':emp.welding_allowance,
                        #         'temp_allowance':emp.temp_allowance
                        #     })
                        # emp.basic = pp[2]
                        # emp.house_rent_allowance = pp[3]
                        # emp.conveyance_allowance = pp[4]
                        # emp.special_allowance = pp[5]
                        # emp.other_allowance = pp[6]
                        # emp.medical_allowance = pp[7]
                        # emp.leave_travel_allowance = pp[8]
                        # emp.position_allowance = pp[9]
                        # emp.children_education = pp[10]
                        # emp.children_hostel = pp[11]
                        # emp.washing_allowance = pp[12]
                        # emp.temp_allowance = pp[13]
                        # emp.service_charge = pp[14]
                        # emp.ppe = pp[15]
                        emp.save(ignore_permissions=True)
                        frappe.db.commit()




@frappe.whitelist()
def get_template():
    args = frappe.local.form_dict

    w = UnicodeWriter()
    w = add_header(w)

    data = get_data(w,args)

    for row in data:
        w.writerow(row)

    # write out response as a type csv
    frappe.response['result'] = cstr(w.getvalue())
    frappe.response['type'] = 'csv'
    frappe.response['doctype'] = "Salary Revision"


def add_header(w):
    w.writerow(['Employee ID','Employee Name','Basic','House Rent Allowance','Conveyance Allowance','Special Allowance','Other Allowance','Medical Allowance','Leave Travel Allowance','Position Allowance','Children Education','Children Hostel','Washing Allowance','Welding Allowance','Temp Allowance','Service Charge','PPE','EPF ER','ESI ER','Gross','CTC'])
    return w


def get_data(w,args):
    data = []
    employees = frappe.db.get_all('Employee',
        fields=['name', 'employee_name'],
        filters={
            'docstatus': ['<', 2],
            'status': 'Active',
            'employee_type': args.employee_type
        }
    )
    for emp in employees:
        data.append([emp.name,emp.employee_name])
    return data