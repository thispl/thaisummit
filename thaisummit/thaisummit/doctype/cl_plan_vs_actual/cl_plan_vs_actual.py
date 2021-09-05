# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from os import PathLike
import frappe
from frappe.model.document import Document

class CLPlanvsActual(Document):
    @frappe.whitelist()
    def get_data(self):
        total_plan = 0
        total_actual = 0
        total_diff = 0
        total_short_percent = 0 
        if self.shift != 'Full Day':
            shift_type = 'shift_' + self.shift.lower()
            data = ''
            data += '<table class="table table-bordered table-sm"><tr style="font-size:8px"><th style="background-color:#ff9900;border: 1px solid black;"><b><center>DATE</center></b></th><th colspan="2" style="background-color:#00b33c;border: 1px solid black"><center><b>%s</b></center></th><th colspan="2" style="background-color:#ff9900;border: 1px solid black"><center><b>SHIFT</b></center></th><th colspan="2" style="background-color:#00b33c;border: 1px solid black"><center><b>%s</b></center></th></tr>'%(frappe.utils.format_date(self.date),self.shift)
            data += '<tr height="10%" style="background-color:#d5dbdb;border: 1px solid black;font-size:8px"><td style="border: 1px solid black"><b><center>CONTRACTOR</center></b></td><td style="border: 1px solid black"><b><center>PLAN</center></b></td><td style="border: 1px solid black"><b><center>ACTUAL</center></b></td><td style="border: 1px solid black"><b><center>DIFF</center></b></td><td style="border: 1px solid black"><b><center>SHORT %</center></b></td><td style="border: 1px solid black"><b><center>OT</center></b></td></tr>'
            contractors = frappe.get_all('Contractor')
            for contractor in contractors:
                plan=frappe.db.sql("select %s as plan from `tabCL Head Count Plan` where contractor = '%s' and date = '%s' "%(shift_type,contractor.name,self.date),as_dict=True)
                if plan:
                    plan = plan[0].plan
                else:
                    plan = 0
                actual = frappe.db.sql("select count(*) as count from `tabQR Checkin` left join `tabEmployee` on `tabQR Checkin`.employee = `tabEmployee`.name where `tabEmployee`.contractor = '%s' and `tabQR Checkin`.qr_shift = '%s' and `tabQR Checkin`.shift_date = '%s' and `tabQR Checkin`.employee_type = 'CL' and `tabQR Checkin`.ot = '0' "%(contractor.name,self.shift,self.date),as_dict=True)
                if actual:
                    actual = actual[0].count
                else:
                    actual = 0
                short = plan - actual
                actual_ot = frappe.db.sql("select count(*) as count from `tabQR Checkin` left join `tabEmployee` on `tabQR Checkin`.employee = `tabEmployee`.name where `tabEmployee`.contractor = '%s' and `tabQR Checkin`.qr_shift = '%s' and `tabQR Checkin`.shift_date = '%s' and `tabQR Checkin`.employee_type = 'CL' and `tabQR Checkin`.ot != 0 "%(contractor.name,self.shift,self.date),as_dict=True)
                if actual_ot[0].count:
                    actual_ot = actual_ot[0].count
                else:
                    actual_ot = 0
                diff = actual - plan
                if diff >= 0:
                    diff_clr = 'black'
                else:
                    diff_clr = 'red'
                if plan > 0:
                    short_percent = (short/plan) * 100
                else:
                    short_percent = 0
                data += '<tr style="font-size:5px;padding:0px"><td style="border: 1px solid black;padding:2px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b style="color:%s"><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td></tr>'%(contractor.name,plan,actual,diff_clr,diff,str(int(short_percent))+'%',actual_ot)
            total_plan = frappe.db.sql("select sum(%s) as total from `tabCL Head Count Plan` where date = '%s' "%(shift_type,self.date),as_dict=True)
            if total_plan[0].total is not None:
                total_plan = total_plan[0].total
            else:
                total_plan = 0
            total_actual = frappe.db.sql("select count(*) as count from `tabQR Checkin` left join `tabEmployee` on `tabQR Checkin`.employee = `tabEmployee`.name where `tabQR Checkin`.qr_shift = '%s' and `tabQR Checkin`.ot = 0 and `tabQR Checkin`.shift_date = '%s' and `tabQR Checkin`.employee_type = 'CL' and `tabEmployee`.contractor is not null "%(self.shift,self.date),as_dict=True)
            total_ot_actual = frappe.db.sql("select count(*) as count from `tabQR Checkin` left join `tabEmployee` on `tabQR Checkin`.employee = `tabEmployee`.name where `tabQR Checkin`.qr_shift = '%s' and `tabQR Checkin`.ot != 0 and `tabQR Checkin`.shift_date = '%s' and `tabQR Checkin`.employee_type = 'CL' and `tabEmployee`.contractor is not null"%(self.shift,self.date),as_dict=True)
            if total_actual[0].count is not None:
                total_actual = total_actual[0].count
            else:
                total_actual = 0
            if total_ot_actual[0].count is not None:
                total_ot_actual = total_ot_actual[0].count
            else:
                total_actual = 0
            total_diff = total_actual - total_plan
            if total_plan > 0:
                total_short_percent = (total_diff/total_plan) * 100
            else:
                total_short_percent = 0
            data += '<tr style="background-color:#ff9900;font-size:10px"><td style="border: 1px solid black"><center><b>Total</b><center></td><td style="border: 1px solid black"><b><center>%s</center></b></td><td style="border: 1px solid black"><b><center>%s</center></b></td><td style="border: 1px solid black"><b><center>%s</center></b></td><td style="border: 1px solid black"><b><center>%s</center></b></td><td style="border: 1px solid black"><b><center>%s</center></b></td></tr>'%(int(total_plan),int(total_actual),total_diff,str(int(total_short_percent))+'%',total_ot_actual)
            data +='</table>'
            return data
        else:
            data = ''
            data += '<table class="table table-bordered table-sm"><tr style="font-size:8px"><th style="background-color:#ff9900;border: 1px solid black;"><b><center>DATE</center></b></th><th colspan="2" style="background-color:#00b33c;border: 1px solid black"><center><b>%s</b></center></th><th colspan="2" style="background-color:#ff9900;border: 1px solid black"><center><b>SHIFT</b></center></th><th colspan="2" style="background-color:#00b33c;border: 1px solid black"><center><b>%s</b></center></th></tr>'%(frappe.utils.format_date(self.date),self.shift)
            data += '<tr height="10%" style="background-color:#d5dbdb;border: 1px solid black;font-size:8px"><td style="border: 1px solid black"><b><center>CONTRACTOR</center></b></td><td style="border: 1px solid black"><b><center>PLAN</center></b></td><td style="border: 1px solid black"><b><center>ACTUAL</center></b></td><td style="border: 1px solid black"><b><center>DIFF</center></b></td><td style="border: 1px solid black"><b><center>SHORT %</center></b></td><td style="border: 1px solid black"><b><center>OT</center></b></td></tr>'
            contractors = frappe.get_all('Contractor')
            for contractor in contractors:
                plan_doc=frappe.db.sql("select * from `tabCL Head Count Plan` where contractor = '%s' and date = '%s' "%(contractor.name,self.date),as_dict=True)
                shift_1 = 0
                shift_2 = 0
                shift_3 = 0
                shift_pp1 = 0
                shift_pp2 = 0
                if plan_doc:
                    if plan_doc[0].shift_1 is not None:
                        shift_1 = plan_doc[0].shift_1
                    if plan_doc[0].shift_2 is not None:
                        shift_2 = plan_doc[0].shift_2
                    if plan_doc[0].shift_3 is not None:
                        shift_3 = plan_doc[0].shift_3
                    if plan_doc[0].shift_pp1 is not None:
                        shift_pp1 = plan_doc[0].shift_pp1
                    if plan_doc[0].shift_pp2 is not None:
                        shift_pp2 = plan_doc[0].shift_pp2
                    plan = shift_1 + shift_2 + shift_3 + shift_pp1 + shift_pp2
                else:
                    plan = 0
                actual = frappe.db.sql("select count(*) as count from `tabQR Checkin` left join `tabEmployee` on `tabQR Checkin`.employee = `tabEmployee`.name where `tabEmployee`.contractor = '%s' and `tabQR Checkin`.shift_date = '%s' and `tabQR Checkin`.employee_type = 'CL' and `tabQR Checkin`.ot = '0' "%(contractor.name,self.date),as_dict=True)
                if actual[0].count is not None:
                    actual = actual[0].count
                else:
                    actual = 0
                short = plan - actual
                actual_ot = frappe.db.sql("select count(*) as count from `tabQR Checkin` left join `tabEmployee` on `tabQR Checkin`.employee = `tabEmployee`.name where `tabEmployee`.contractor = '%s' and `tabQR Checkin`.shift_date = '%s' and `tabQR Checkin`.employee_type = 'CL' and `tabQR Checkin`.ot != 0 "%(contractor.name,self.date),as_dict=True)
                if actual_ot[0].count is not None:
                    actual_ot = actual_ot[0].count
                else:
                    actual_ot = 0
                diff = actual - plan
                if diff >= 0:
                    diff_clr = 'black'
                else:
                    diff_clr = 'red'
                if plan > 0:
                    short_percent = (short/plan) * 100
                else:
                    short_percent = 0
                data += '<tr style="font-size:5px;padding:0px"><td style="border: 1px solid black;padding:2px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b style="color:%s"><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td></tr>'%(contractor.name,plan,actual,diff_clr,diff,str(int(short_percent))+'%',actual_ot)
            total_plan_doc = frappe.db.sql("select sum(shift_1) as shift_1,sum(shift_2) as shift_2,sum(shift_3) as shift_3,sum(shift_pp1) as shift_pp1,sum(shift_pp2) as shift_pp2 from `tabCL Head Count Plan` where date = '%s' "%(self.date),as_dict=True)
            if total_plan_doc:
                shift_1 = 0
                shift_2 = 0
                shift_3 = 0
                shift_pp1 = 0
                shift_pp2 = 0
                if total_plan_doc[0].shift_1 is not None:
                    shift_1 = total_plan_doc[0].shift_1
                if total_plan_doc[0].shift_2 is not None:
                    shift_2 = total_plan_doc[0].shift_2
                if total_plan_doc[0].shift_3 is not None:
                    shift_3 = total_plan_doc[0].shift_3
                if total_plan_doc[0].shift_pp1 is not None:
                    shift_pp1 = total_plan_doc[0].shift_pp1
                if total_plan_doc[0].shift_pp2 is not None:
                    shift_pp2 = total_plan_doc[0].shift_pp2
                total_plan = shift_1 + shift_2 + shift_3 + shift_pp1 + shift_pp2
            else:
                total_plan = 0
            total_actual = frappe.db.sql("select count(*) as count from `tabQR Checkin` left join `tabEmployee` on `tabQR Checkin`.employee = `tabEmployee`.name where `tabQR Checkin`.ot = 0 and `tabQR Checkin`.shift_date = '%s' and `tabQR Checkin`.employee_type = 'CL' and `tabEmployee`.contractor is not null "%(self.date),as_dict=True)
            total_ot_actual = frappe.db.sql("select count(*) as count from `tabQR Checkin` left join `tabEmployee` on `tabQR Checkin`.employee = `tabEmployee`.name where `tabQR Checkin`.ot != 0 and `tabQR Checkin`.shift_date = '%s' and `tabQR Checkin`.employee_type = 'CL' and `tabEmployee`.contractor is not null"%(self.date),as_dict=True)
            if total_actual[0].count is not None:
                total_actual = total_actual[0].count
            else:
                total_actual = 0
            if total_ot_actual[0].count is not None:
                total_ot_actual = total_ot_actual[0].count
            else:
                total_actual = 0
            total_diff = total_actual - total_plan
            if total_plan > 0:
                total_short_percent = (total_diff/total_plan) * 100
            else:
                total_short_percent = 0
            data += '<tr style="background-color:#ff9900;font-size:10px"><td style="border: 1px solid black"><center><b>Total</b><center></td><td style="border: 1px solid black"><b><center>%s</center></b></td><td style="border: 1px solid black"><b><center>%s</center></b></td><td style="border: 1px solid black"><b><center>%s</center></b></td><td style="border: 1px solid black"><b><center>%s</center></b></td><td style="border: 1px solid black"><b><center>%s</center></b></td></tr>'%(int(total_plan),int(total_actual),total_diff,str(int(total_short_percent))+'%',total_ot_actual)
            data +='</table>'
            return data
