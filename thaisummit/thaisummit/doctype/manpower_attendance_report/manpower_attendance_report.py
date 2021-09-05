# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ManpowerAttendanceReport(Document):
    pass


@frappe.whitelist()
def manpower_attendance_report(doc,depts):
    data = ''
    for dept in depts:
        data += "<tr><td>%s</td>"%dept
        wc = frappe.db.count("Attendance",{'employee_type':'WC',"shift":doc.shift,"attendance_date":doc.date,"Department":dept})
        data += "<td>%s</td>"%wc
        emp_type = ["BC","NT","FT","CL"]
        for e in emp_type:
            c = frappe.db.count("Attendance",{'employee_type':e,"qr_shift":doc.shift,"attendance_date":doc.date,"Department":dept})
            data += "<td>%s</td>"%c
        qc = frappe.db.count("Attendance",{'employee_type':['!=','WC'],"qr_shift":doc.shift,"attendance_date":doc.date,"Department":dept})
        data += "<td>%s</td>"%(wc+qc)
        
        ### BC FC NT CL count

        bfnc_plan =  frappe.db.count("Shift Assignment",{'employee_type':['!=','WC'],"shift_type":doc.shift,"start_date":doc.date,"Department":dept})
        data += "<td>%s</td>"%bfnc_plan
        bfnc_actual = frappe.db.count("Attendance",{'employee_type':['!=','WC'],"qr_shift":doc.shift,"attendance_date":doc.date,"Department":dept})
        data += "<td>%s</td>"%bfnc_actual
        bfnc_diff = bfnc_actual - bfnc_plan
        data += "<td style='background-color:#DE3163'>%s</td>"%bfnc_diff
        if bfnc_plan != 0:
            bfnc_percent = (bfnc_diff*100)/bfnc_plan
        else:
            bfnc_percent = '-'
        data += "<td style='background-color:#DE3163'>%s</td>"%bfnc_percent
        bfnc_ot = 0
        data += "<td>%s</td>"%bfnc_ot

        emp_type = ["BC","NT","FT","CL"]
        for e in emp_type:
            plan =  frappe.db.count("Shift Assignment",{'employee_type':e,"shift_type":doc.shift,"start_date":doc.date,"Department":dept})
            data += "<td>%s</td>"%plan
            actual = frappe.db.count("Attendance",{'employee_type':e,"qr_shift":doc.shift,"attendance_date":doc.date,"Department":dept})
            data += "<td>%s</td>"%actual
            diff = actual - plan
            data += "<td style='background-color:#DE3163'>%s</td>"%diff
            if plan != 0:
                percent = (diff*100)/plan
            else:
                percent = '-'
            data += "<td style='background-color:#DE3163'>%s</td>"%percent
        data += "</tr>"
    return data


@frappe.whitelist()
def manpower_attendance_report_total(doc,depts,title):
    data = ''
    data += "<tr><td style='background-color:#f1948a'>%s</td>"%title
    wc = frappe.db.count("Attendance",{'employee_type':'WC',"shift":doc.shift,"attendance_date":doc.date,"Department":['in',depts]})
    data += "<td style='background-color:#228B22'>%s</td>"%wc
    emp_type = ["BC","NT","FT","CL"]
    for e in emp_type:
        c = frappe.db.count("Attendance",{'employee_type':e,"qr_shift":doc.shift,"attendance_date":doc.date,"Department":['in',depts]})
        data += "<td style='background-color:#228B22'>%s</td>"%c
    qc = frappe.db.count("Attendance",{'employee_type':['!=','WC'],"qr_shift":doc.shift,"attendance_date":doc.date,"Department":['in',depts]})
    data += "<td style='background-color:#228B22'>%s</td>"%(wc+qc)
        
    ### BC FC NT CL count

    bfnc_plan =  frappe.db.count("Shift Assignment",{'employee_type':['!=','WC'],"shift_type":doc.shift,"start_date":doc.date,"Department":['in',depts]})
    data += "<td style='background-color:#85c1e9'>%s</td>"%bfnc_plan
    bfnc_actual = frappe.db.count("Attendance",{'employee_type':['!=','WC'],"qr_shift":doc.shift,"attendance_date":doc.date,"Department":['in',depts]})
    data += "<td style='background-color:#85c1e9'>%s</td>"%bfnc_actual
    bfnc_diff = bfnc_actual - bfnc_plan
    data += "<td style='background-color:#85c1e9'>%s</td>"%bfnc_diff
    if bfnc_plan != 0:
        bfnc_percent = (bfnc_diff*100)/bfnc_plan
    else:
        bfnc_percent = '-'
    data += "<td style='background-color:#85c1e9'>%s</td>"%bfnc_percent
    bfnc_ot = 0
    data += "<td style='background-color:#85c1e9'>%s</td>"%bfnc_ot

    emp_type = ["BC","NT","FT","CL"]
    for e in emp_type:
        if e == 'BC':
            bg = '#85c1e9'
        elif e == 'NT':
            bg = '#f5cba7'
        elif e == 'FT':
            bg = '#d98880'
        elif e == 'CL':
            bg = '#f8c471'
        plan =  frappe.db.count("Shift Assignment",{'employee_type':e,"shift_type":doc.shift,"start_date":doc.date,"Department":['in',depts]})
        data += "<td style='background-color:%s'>%s</td>"%(bg,plan)
        actual = frappe.db.count("Attendance",{'employee_type':e,"qr_shift":doc.shift,"attendance_date":doc.date,"Department":['in',depts]})
        data += "<td style='background-color:%s'>%s</td>"%(bg,actual)
        diff = actual - plan
        data += "<td style='background-color:%s'>%s</td>"%(bg,diff)
        if plan != 0:
            percent = (diff*100)/plan
        else:
            percent = '-'
        data += "<td style='background-color:%s'>%s</td>"%(bg,percent)
    data += "</tr>"
    return data
