# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ManpowerAttendanceReport(Document):
    pass


@frappe.whitelist()
def manpower_attendance_report(doc):
    re_depts =  ["WELD-RE - TSAIP","Weld-RE P1E","Weld-RE J LINE - TSAIP","WELD-RE J LINE 2 - TSAIP","PRESS-RE - TSAIP","Total DIRECT RE"]
    re_dept_list = [["WELD-RE - TSAIP"],["Weld-RE P1E"],["Weld-RE J LINE - TSAIP"],["WELD-RE J LINE 2 - TSAIP"],["PRESS-RE - TSAIP"],["Total DIRECT RE"]]
    i = 0
    for dept in re_depts:
        if dept != "Total DIRECT RE":
            c = frappe.db.count("Attendance",{'employee_type':'WC',"shift":"1","attendance_date":doc.date,"Department":dept})
            re_dept_list[i].append(c)
            emp_type = ["BC","NT","FT","CL"]
            for e in emp_type:
                c = frappe.db.count("QR Checkin",{'employee_type':e,"qr_shift":"1","shift_date":doc.date,"Department":dept})
                re_dept_list[i].append(c)
            c = frappe.db.count("QR Checkin",{'employee_type':['!=','WC'],"qr_shift":"1","shift_date":doc.date,"Department":dept})
            re_dept_list[i].append(c)
            
            # BC FC NT CL count

            bfnc_plan =  frappe.db.count("Shift Assignment",{'employee_type':['!=','WC'],"shift_type":"1","start_date":doc.date,"Department":dept})
            re_dept_list[i].append(bfnc_plan)
            bfnc_actual = frappe.db.count("QR Checkin",{'employee_type':['!=','WC'],"qr_shift":"1","shift_date":doc.date,"Department":dept})
            re_dept_list[i].append(bfnc_actual)
            bfnc_diff = bfnc_actual - bfnc_plan
            re_dept_list[i].append(bfnc_diff)
            if bfnc_plan != 0:
                bfnc_percent = (bfnc_diff*100)/bfnc_plan
            else:
                bfnc_percent = '-'
            re_dept_list[i].append(bfnc_percent)
            bfnc_ot = 0
            re_dept_list[i].append(bfnc_ot)

            # BC Count
            bc_plan = 0
            re_dept_list[i].append(bc_plan)
            bc_actual = 0
            re_dept_list[i].append(bc_actual)
            bc_diff = bc_actual - bc_plan
            re_dept_list[i].append(bc_diff)
            if bc_plan != 0:
                bc_percent = (bc_diff*100)/bc_plan
            else:
                bc_percent = '-'
            re_dept_list[i].append(bc_percent)

            # NT Count
            nt_plan = 0
            re_dept_list[i].append(nt_plan)
            nt_actual = 0
            re_dept_list[i].append(nt_actual)
            nt_diff = nt_actual - nt_plan
            re_dept_list[i].append(nt_diff)
            if nt_plan != 0:
                nt_percent = (nt_diff*100)/nt_plan
            else:
                nt_percent = '-'
            re_dept_list[i].append(nt_percent)

            # FT Count
            ft_plan = 0
            re_dept_list[i].append(ft_plan)
            ft_actual = 0
            re_dept_list[i].append(ft_actual)
            ft_diff = ft_actual - ft_plan
            re_dept_list[i].append(ft_diff)
            if ft_plan != 0:
                ft_percent = (ft_diff*100)/ft_plan
            else:
                ft_percent = '-'
            re_dept_list[i].append(ft_percent)

            # CL Count
            cl_plan = 0
            re_dept_list[i].append(cl_plan)
            cl_actual = 0
            re_dept_list[i].append(cl_actual)
            cl_diff = cl_actual - cl_plan
            re_dept_list[i].append(cl_diff)
            if cl_plan != 0:
                cl_percent = (cl_diff*100)/cl_plan
            else:
                cl_percent = '-'
            re_dept_list[i].append(cl_percent)

            # total direct RE
        elif dept == "Total DIRECT RE":
            c = frappe.db.count("Attendance",{'employee_type':'WC',"shift":"1","attendance_date":doc.date,"Department":['in',re_depts]})
            frappe.errprint(re_dept_list[i])
            re_dept_list[i].append(c)
            frappe.errprint(i)
            frappe.errprint(c)
            frappe.errprint(re_dept_list[i])
            emp_type = ["BC","NT","FT","CL"]
            for e in emp_type:
                c = frappe.db.count("QR Checkin",{'employee_type':e,"qr_shift":"1","shift_date":doc.date,"Department":['in',re_depts]})
                re_dept_list[i].append(c)
            c = frappe.db.count("QR Checkin",{'employee_type':['!=','WC'],"qr_shift":"1","shift_date":doc.date,"Department":['in',re_depts]})
            re_dept_list[i].append(c)
            
            # BC FC NT CL count

            bfnc_plan =  frappe.db.count("Shift Assignment",{'employee_type':['!=','WC'],"shift_type":"1","start_date":doc.date,"Department":re_depts})
            re_dept_list[i].append(bfnc_plan)
            bfnc_actual = frappe.db.count("QR Checkin",{'employee_type':['!=','WC'],"qr_shift":"1","shift_date":doc.date,"Department":re_depts})
            re_dept_list[i].append(bfnc_actual)
            bfnc_diff = bfnc_actual - bfnc_plan
            re_dept_list[i].append(bfnc_diff)
            if bfnc_plan != 0:
                bfnc_percent = (bfnc_diff*100)/bfnc_plan
            else:
                bfnc_percent = '-'
            re_dept_list[i].append(bfnc_percent)
            bfnc_ot = 0
            re_dept_list[i].append(bfnc_ot)

            # BC Count
            bc_plan = 0
            re_dept_list[i].append(bc_plan)
            bc_actual = 0
            re_dept_list[i].append(bc_actual)
            bc_diff = bc_actual - bc_plan
            re_dept_list[i].append(bc_diff)
            if bc_plan != 0:
                bc_percent = (bc_diff*100)/bc_plan
            else:
                bc_percent = '-'
            re_dept_list[i].append(bc_percent)

            # NT Count
            nt_plan = 0
            re_dept_list[i].append(nt_plan)
            nt_actual = 0
            re_dept_list[i].append(nt_actual)
            nt_diff = nt_actual - nt_plan
            re_dept_list[i].append(nt_diff)
            if nt_plan != 0:
                nt_percent = (nt_diff*100)/nt_plan
            else:
                nt_percent = '-'
            re_dept_list[i].append(nt_percent)

            # FT Count
            ft_plan = 0
            re_dept_list[i].append(ft_plan)
            ft_actual = 0
            re_dept_list[i].append(ft_actual)
            ft_diff = ft_actual - ft_plan
            re_dept_list[i].append(ft_diff)
            if ft_plan != 0:
                ft_percent = (ft_diff*100)/ft_plan
            else:
                ft_percent = '-'
            re_dept_list[i].append(ft_percent)

            # CL Count
            cl_plan = 0
            re_dept_list[i].append(cl_plan)
            cl_actual = 0
            re_dept_list[i].append(cl_actual)
            cl_diff = cl_actual - cl_plan
            re_dept_list[i].append(cl_diff)
            if cl_plan != 0:
                cl_percent = (cl_diff*100)/cl_plan
            else:
                cl_percent = '-'
            re_dept_list[i].append(cl_percent)

        i += 1
    re_support_depts =  ["QA-RE - TSAIP","PPC-RE - TSAIP","BOP-RE - TSAIP","NPD-RE - TSAIP","JIGS MTN-RE - TSAIP","SALES-RE - TSAIP","TOTAL SUPPORT RE","GRAND TOTAL RE"]
    re_support_dept_list = [["QA-RE - TSAIP"],["PPC-RE - TSAIP"],["BOP-RE - TSAIP"],["NPD-RE - TSAIP"],["JIGS MTN-RE - TSAIP"],["SALES-RE - TSAIP"],["TOTAL SUPPORT RE"],["GRAND TOTAL RE"]]
    i = 0
    # print(re_dept_list)
    return re_dept_list