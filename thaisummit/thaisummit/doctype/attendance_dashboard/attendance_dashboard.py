# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date, timedelta,time
import datetime
from datetime import datetime
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)


class AttendanceDashboard(Document):
    pass
    

@frappe.whitelist()
def get_shift(emp,month,year):
    month_dict = [{'Jan':'1','Feb':'2','Mar':'3','Apr':'4','May':'5','Jun':'6','Jul':'7','Aug':'8','Sep':'9','Oct':'10','Nov':'11','Dec':'12'}]
    month_no = [ m[month] for m in month_dict ]
    date = str(year) + "-" + str(month_no[0])+ "-" + str(1)
    date = datetime.strptime(date,'%Y-%m-%d')
    previous_month = frappe.utils.add_months(date, -1).strftime("%Y-%m-26")
    current_month = date.strftime("%Y-%m-25")
    date_list = get_dates(previous_month,current_month)
    data = ''
    rh1 = '<tr>'
    rh2 = ''
    rh3 = ''
    rd1 = '<tr>'
    rd2 = ''
    rd3 = ''
    r1 = ''
    r2 = ''
    r3 = ''
    i = 1
    for date in date_list:
        if frappe.db.exists('Attendance',{'employee':emp,'attendance_date':date,'docstatus':['!=','2']}):
            att = frappe.get_doc('Attendance',{'employee':emp,'attendance_date':date,'docstatus':['!=','2']})
            status = ''
            if att.employee_type != "WC":
                if not att.in_time or not att.out_time:
                    if att.qr_shift:
                        status = "M" + str(att.qr_shift)
                    else:
                        status = "AA"
                if att.in_time and att.out_time:
                    if not att.qr_shift:
                        status = str(att.shift) + "M"
                    elif att.late_entry == '1':
                        status = str(att.shift) + 'L' + "M"
                    else:
                        status = str(att.shift) + str(att.qr_shift)
                if att.status == 'On Leave':
                    status = att.leave_type
                if att.on_duty_application:
                    status = "OD"
            else:
                if att.status == 'On Leave':
                    status = att.leave_type
                if att.on_duty_application:
                    status = "OD"
                if att.shift:
                    if att.late_entry == '1':
                        status = str(att.shift) + 'L' + str(att.shift)
                    elif att.in_time:
                        if not att.out_time:
                            status = str(att.shift) + 'M'
                        else:
                            status = str(att.shift) + str(att.shift)
                    elif att.out_time:
                        if not att.in_time:
                            status =  'M' + str(att.shift)
                        else:    
                            status = str(att.shift) + str(att.shift)

            if i <= 10:
                rh1 += """<th style = 'border: 1px solid black;background-color:#ffedcc;'><center>%s</center></th>"""%((datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                if status:
                    rd1 += """<td style = 'border: 1px solid black'><center>%s</center></td>"""%(status)
                else:
                    holiday = check_holiday(date)
                    if holiday:
                        rd1 += """<td style = 'border: 1px solid black'><center><b>%s</b></center></td>"""%(holiday)
                    else:
                        rd1 += """<td style = 'border: 1px solid black'><center><b><p style="color:red;">A</p></b></center></td>"""
                if i == 10:
                    r1 = rh1 + '</tr>' + rd1 + '</tr>'
            elif 10 < i <= 20:
                rh2 += """<th style = 'border: 1px solid black;background-color:#ffedcc;'><center>%s</center></th>"""%((datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                if status:
                    rd2 += """<td style = 'border: 1px solid black'><center>%s</center></td>"""%(status)
                else:
                    holiday = check_holiday(date)
                    if holiday:
                        rd2 += """<td style = 'border: 1px solid black'><center><b>%s</b></center></td>"""%(holiday)
                    else:
                        rd2 += """<td style = 'border: 1px solid black'><center><b><p style="color:red;">A</p></b></center></td>"""
                if i == 20:
                    r2 = '<tr>' + rh2 + '</tr><tr>' + rd2 + '</tr>'
            elif 20 < i:
                rh3 += """<th style = 'border: 1px solid black;background-color:#ffedcc;'><center>%s</center></th>"""%((datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                if status:
                    rd3 += """<td style = 'border: 1px solid black'><center>%s</center></td>"""%(status)
                else:
                    holiday = check_holiday(date)
                    if holiday:
                        rd3 += """<td style = 'border: 1px solid black'><center><b>%s</b></center></td>"""%(holiday)
                    else:
                        rd3 += """<td style = 'border: 1px solid black'><center><b><p style="color:red;">A</p></b></center></td>"""
            i += 1
        else:
            if i <= 10:
                rh1 += """<th style = 'border: 1px solid black;background-color:#ffedcc;'><center>%s</center></th>"""%((datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                rd1 += """<td style = 'border: 1px solid black'><center>-</center></td>"""
                r1 = rh1 + '</tr>' + rd1 + '</tr>'
            elif 10 < i <= 20:
                rh2 += """<th style = 'border: 1px solid black;background-color:#ffedcc;'><center>%s</center></th>"""%((datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                rd2 += """<td style = 'border: 1px solid black'><center>-</center></td>"""
                if i == 20:
                    r2 = '<tr>' + rh2 + '</tr><tr>' + rd2 + '</tr>'
            elif 20 < i:
                rh3 += """<th style = 'border: 1px solid black;background-color:#ffedcc;'><center>%s</center></th>"""%((datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                rd3 += """<td style = 'border: 1px solid black'><center>-</center></td>"""
            i += 1
        data = "<h3>Attendance Summary</h3><table border='1px' class='table table-bordered'>" + r1 + r2 + '<tr>' + rh3 + '</tr><tr>' + rd3 + '</tr>' +"</table>"

    return data
def get_dates(previous_month,current_month):
    """get list of dates in between from date and to date"""
    no_of_days = date_diff(add_days(current_month, 1),previous_month )
    dates = [add_days(previous_month, i) for i in range(0, no_of_days)]
    return dates

def check_holiday(date):
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = 'Holiday List - 2021' and holiday_date = '%s' """%(date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            return "HH"

@frappe.whitelist()
def get_ot(emp,month,year):
    month_dict = [{'Jan':'1','Feb':'2','Mar':'3','Apr':'4','May':'5','Jun':'6','Jul':'7','Aug':'8','Sep':'9','Oct':'10','Nov':'11','Dec':'12'}]
    month_no = [ m[month] for m in month_dict ]
    date = str(year) + "-" + str(month_no[0])+ "-" + str(1)
    date = datetime.strptime(date,'%Y-%m-%d')
    previous_month = frappe.utils.add_months(date, -1).strftime("%Y-%m-26")
    current_month = date.strftime("%Y-%m-25")
    date_list = get_dates(previous_month,current_month)
    data = ''
    rh1 = '<tr>'
    rh2 = ''
    rh3 = ''
    rd1 = '<tr>'
    rd2 = ''
    rd3 = ''
    r1 = ''
    r2 = ''
    r3 = ''
    i = 1
    total_ot = timedelta(0,0,0)
    for date in date_list:
        if frappe.db.exists('Overtime Request',{'employee':emp,'ot_date':date,'workflow_state':'Approved'}):
            ot = frappe.db.get_value('Overtime Request',{'employee':emp,'ot_date':date,'workflow_state':'Approved'},'ot_hours')
            total_ot = total_ot + ot
            if i <= 10:
                rh1 += """<th style = 'border: 1px solid black;background-color:#ffedcc;'><center>%s</center></th>"""%((datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                rd1 += """<td style = 'border: 1px solid black'><center>%s</center></td>"""%(ot or 'A')
                r1 = rh1 + '</tr>' + rd1 + '</tr>'
            elif 10 < i <= 20:
                rh2 += """<th style = 'border: 1px solid black;background-color:#ffedcc;'><center>%s</center></th>"""%((datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                rd2 += """<td style = 'border: 1px solid black'><center>%s</center></td>"""%(ot or 'A')
                if i == 20:
                    r2 = '<tr>' + rh2 + '</tr><tr>' + rd2 + '</tr>'
            elif 20 < i:
                rh3 += """<th style = 'border: 1px solid black;background-color:#ffedcc;'><center>%s</center></th>"""%((datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                rd3 += """<td style = 'border: 1px solid black'><center>%s</center></td>"""%(ot or 'A')
            i += 1
        else:
            if i <= 10:
                rh1 += """<th style = 'border: 1px solid black;background-color:#ffedcc;'><center>%s</center></th>"""%((datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                rd1 += """<td style = 'border: 1px solid black'><center>-</center></td>"""
                r1 = rh1 + '</tr>' + rd1 + '</tr>'
            elif 10 < i <= 20:
                rh2 += """<th style = 'border: 1px solid black;background-color:#ffedcc;'><center>%s</center></th>"""%((datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                rd2 += """<td style = 'border: 1px solid black'><center>-</center></td>"""
                if i == 20:
                    r2 = '<tr>' + rh2 + '</tr><tr>' + rd2 + '</tr>'
            elif 20 < i:
                rh3 += """<th style = 'border: 1px solid black;background-color:#ffedcc;'><center>%s</center></th>"""%((datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                rd3 += """<td style = 'border: 1px solid black'><center>-</center></td>"""
            i += 1
    day = total_ot.days * 24
    hours = day + total_ot.seconds // 3600
    minutes = (total_ot.seconds//60)%60
    data = "<h3>Overtime Summary </h3><p style='font-size:25px'> Total OT : "+ str(hours) + 'hr ' + str(minutes) + 'min' + "</p><table border='1' class='table table-bordered'>" + r1 + r2 + '<tr>' + rh3 + '</tr><tr>' + rd3 + '</tr>' +"</table>"
    return data
def get_dates(previous_month,current_month):
    """get list of dates in between from date and to date"""
    no_of_days = date_diff(add_days(current_month, 1),previous_month )
    dates = [add_days(previous_month, i) for i in range(0, no_of_days)]
    return dates


