import frappe
import json
import datetime
from frappe.utils.csvutils import read_csv_content
from six.moves import range
from six import string_types
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours
import requests
from datetime import date, timedelta,time

@frappe.whitelist()
def mark_att(from_date):
    mark_on_duty(from_date)
    checkins = frappe.db.sql(
        """select * from `tabEmployee Checkin` where skip_auto_attendance = 0 and date(time) = '%s' """%(from_date),as_dict=1)
    if checkins:
        for c in checkins:
            att = mark_attendance_from_checkin(c.name,c.employee,c.log_type,c.time)
            # print(att)
            if att:
                frappe.db.set_value("Employee Checkin",
                                    c.name, "skip_auto_attendance", "1")
        mark_permission(from_date)
        mark_absent(from_date)
        frappe.msgprint("Attendance Marked Successfully")
        return "ok"
        
    else:
        frappe.msgprint("Attendance Already Marked")

def mark_attendance_from_checkin(checkin,employee,log_type,time):
    att_time = time.time()
    att_date = time.date()
    month_start_date = get_first_day(att_date)
    month_end_date = get_last_day(att_date)
    shift = ''
    if log_type == 'IN':
        min_in_time = ''
        max_in_time = ''
        min_in_time1 = datetime.strptime('06:00', '%H:%M').time()
        max_in_time1 = datetime.strptime('13:00', '%H:%M').time()
        min_in_time2 = datetime.strptime('14:30', '%H:%M').time()
        max_in_time2 = datetime.strptime('18:30', '%H:%M').time()
        min_in_time3 = datetime.strptime('00:01', '%H:%M').time()
        max_in_time3 = datetime.strptime('03:00', '%H:%M').time()
        min_in_timepp1 = datetime.strptime('06:00', '%H:%M').time()
        max_in_timepp1 = datetime.strptime('10:00', '%H:%M').time()
        min_in_timepp2 = datetime.strptime('18:00', '%H:%M').time()
        max_in_timepp2 = datetime.strptime('22:00', '%H:%M').time()
        late1 = datetime.strptime('08:10', '%H:%M').time()
        late2 = datetime.strptime('16:40', '%H:%M').time()
        late3 = datetime.strptime('01:10', '%H:%M').time()
        latepp1 = datetime.strptime('08:10', '%H:%M').time()
        latepp2 = datetime.strptime('20:10', '%H:%M').time()
        late = 0
        status = 'Present'
        if max_in_time1 >= att_time >= min_in_time1:
            if frappe.db.get_value('Employee',employee,"default_shift") == 'PP1':
                shift = 'PP1'
            else:
                shift = '1'
            min_in_time = datetime.strptime('06:00', '%H:%M').time()
            max_in_time = datetime.strptime('13:00', '%H:%M').time()
            if datetime.strptime('08:00', '%H:%M').time() <= att_time <= datetime.strptime('08:10', '%H:%M').time():
                late = 1
            elif att_time > datetime.strptime('08:00', '%H:%M').time():
                status = 'Half Day'
        elif max_in_time2 >= att_time >= min_in_time2:
            shift = '2'
            min_in_time = datetime.strptime('14:30', '%H:%M').time()
            max_in_time = datetime.strptime('18:30', '%H:%M').time()
            if datetime.strptime('16:30', '%H:%M').time() <= att_time <= datetime.strptime('16:40', '%H:%M').time():
                late = 1
            elif att_time > datetime.strptime('16:30', '%H:%M').time():
                status = 'Half Day'
        elif max_in_time3 >= att_time >= min_in_time3:
            shift = '3'
            att_date = add_days(att_date,-1)
            min_in_time = datetime.strptime('00:01', '%H:%M').time()
            max_in_time = datetime.strptime('03:00', '%H:%M').time()
            if datetime.strptime('01:00', '%H:%M').time() <= att_time <= datetime.strptime('01:10', '%H:%M').time():
                late = 1
            elif att_time > datetime.strptime('01:00', '%H:%M').time():
                status = 'Half Day'
        elif max_in_timepp2 >= att_time >= min_in_timepp2:
            shift = 'PP2'
            min_in_time = datetime.strptime('20:00', '%H:%M').time()
            max_in_time = datetime.strptime('22:00', '%H:%M').time()
            if datetime.strptime('20:00', '%H:%M').time() <= att_time <= datetime.strptime('20:10', '%H:%M').time():
                late = 1
            elif att_time > datetime.strptime('20:00', '%H:%M').time():
                status = 'Half Day'
        if late == 1:
            count = frappe.db.sql("select count(*) as count from `tabAttendance` where employee = '%s' and docstatus != 2 and late_entry =1 and attendance_date between '%s' and '%s' "%(employee,month_start_date,month_end_date),as_dict = True)
            if count[0].count:
                if int(count[0].count) >= 2:
                    status = 'Half Day'
        if min_in_time and max_in_time:
            if not frappe.db.exists("Attendance",{'employee':employee,'attendance_date':att_date,'docstatus': ['!=',2]}):
                if shift != '3':
                    checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s' order by time "%(employee,att_date,min_in_time,max_in_time),as_dict=True)
                else:
                    yesterday = add_days(att_date,1)
                    checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s' order by time "%(employee,yesterday,min_in_time,max_in_time),as_dict=True)
                if checkins:    
                    qr_checkin = frappe.db.sql("select name, employee,qr_shift,qr_scan_time,shift_date from `tabQR Checkin` where employee = '%s' and date(qr_scan_time) = '%s' order by qr_scan_time "%(employee,att_date),as_dict=True)
                    att = frappe.new_doc("Attendance")
                    att.employee = employee
                    att.attendance_date = att_date
                    att.shift = shift
                    att.status = status
                    att.late_entry = late
                    att.in_time = checkins[0].time
                    att.shift_status = shift
                    if qr_checkin:
                        att.qr_shift = qr_checkin[0].qr_shift
                        att.qr_scan_time = qr_checkin[0].qr_scan_time
                        att.shift_status = str(shift) + str(qr_checkin[0].qr_shift)
                    att.save(ignore_permissions=True)
                    frappe.db.commit()
                    frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
                    if qr_checkin:
                        frappe.db.set_value("QR Checkin",qr_checkin[0].name, "attendance", att.name)
                    return att
    if log_type == 'OUT':
        max_out = datetime.strptime('10:00', '%H:%M').time()
        if att_time < max_out:
            yesterday = add_days(att_date,-1)
            checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'OUT' and date(time) = '%s' and time(time) < '%s' order by time "%(employee,att_date,max_out),as_dict=True)
            att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':yesterday})
            if att:
                att = frappe.get_doc("Attendance",att)
                if not att.out_time:
                    if att.docstatus == 0:
                        print(att.out_time)
                        if len(checkins) > 0:
                            att.out_time = checkins[-1].time
                        else:
                            att.out_time = checkins[0].time
                        att.save(ignore_permissions=True)
                        if att.shift == att.qr_shift:
                            att.submit()
                        frappe.db.commit()
                        frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
                        return att
            else:
                att = frappe.new_doc("Attendance")
                att.employee = employee
                att.attendance_date = yesterday
                # att.shift_type = shift
                att.status = 'Absent'
                if len(checkins) > 0:
                    att.out_time = checkins[-1].time
                else:
                    att.out_time = checkins[0].time
                att.save(ignore_permissions=True)
                frappe.db.commit()
                frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
                return att
        else:
            checkins = frappe.db.sql("select name,time,docstatus from `tabEmployee Checkin` where employee ='%s' and log_type = 'OUT' and date(time) = '%s' order by time "%(employee,att_date),as_dict=True)
            att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':att_date})
            if att:
                att = frappe.get_doc("Attendance",att)
                if not att.out_time:
                    if att.docstatus == 0:
                        if len(checkins) > 0:
                            att.out_time = checkins[-1].time
                        else:
                            att.out_time = checkins[0].time
                        att.save(ignore_permissions=True)
                        if att.shift == att.qr_shift:
                            att.submit()
                        frappe.db.commit()
                        frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
                        return att
            else:
                att = frappe.new_doc("Attendance")
                att.employee = employee
                att.attendance_date = att_date
                # att.shift_type = shift
                att.status = 'Absent'
                if len(checkins) > 0:
                    att.out_time = checkins[-1].time
                else:
                    att.out_time = checkins[0].time
                att.save(ignore_permissions=True)
                frappe.db.commit()
                frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
                return att

def mark_absent(from_date):
    emps = frappe.get_all("Employee",{'status':'Active','vacant':'0'})
    for emp in emps:
        frappe.errprint(emp.name)
        if not frappe.db.exists('Attendance',{'attendance_date':from_date,'employee':emp.name}):
            doc = frappe.new_doc('Attendance')
            doc.employee = emp.name
            doc.status = 'Absent'
            doc.attendance_date = from_date
            doc.save(ignore_permissions=True)
            doc.submit()
            frappe.db.commit()
    

def mark_on_duty(from_date):
    ods = frappe.db.sql("""select `tabOn Duty Application`.name, `tabOn Duty Application`.from_date,`tabOn Duty Application`.workflow_state,`tabOn Duty Application`.to_date,`tabMulti Employee`.employee
    from `tabOn Duty Application`
    left join `tabMulti Employee` on `tabOn Duty Application`.name = `tabMulti Employee`.parent
    where '%s' between from_date and to_date and workflow_state = 'Approved' """%(from_date),as_dict=True)
    for od in ods:
        att = frappe.new_doc("Attendance")
        att.employee = od.employee
        att.status = "Present"
        att.attendance_date = from_date
        att.on_duty_application = od.name
        att.save(ignore_permissions=True)
        att.submit()
        frappe.db.commit()

def mark_permission(from_date):
    pr_list = frappe.db.sql("""SELECT employee,attendance_date,shift,session FROM `tabPermission Request` 
    WHERE docstatus=1 and workflow_state = 'Approved' and attendance_date = '%s' """%from_date,as_dict=True)
    for pr in pr_list:
        print(pr)
        attendance = frappe.db.exists("Attendance",{"employee": pr.employee,"attendance_date":pr.attendance_date,"docstatus":['!=',2]})
        if attendance:
            att = frappe.get_doc("Attendance",attendance)
            if att.in_time and att.out_time:
                in_t = datetime.strptime(str(att.in_time.time()), '%H:%M:%S')
                out_t = datetime.strptime(str(att.out_time.time()), '%H:%M:%S')
                if pr.session == 'First Half':
                    if pr.shift == '1':
                        shift_in = datetime.strptime('08:00', '%H:%M')
                        diff = time_diff_in_hours(in_t,shift_in)
                    elif pr.shift == '2':
                        shift_in = datetime.strptime('16:30', '%H:%M')
                        diff = time_diff_in_hours(in_t,shift_in)
                    elif pr.shift == '3':
                        shift_in = datetime.strptime('01:00', '%H:%M')
                        diff = time_diff_in_hours(in_t,shift_in)
                    elif pr.shift == 'PP1':
                        shift_in = datetime.strptime('08:00', '%H:%M')
                        diff = time_diff_in_hours(in_t,shift_in)
                    elif pr.shift == 'PP2':
                        shift_in = datetime.strptime('20:00', '%H:%M')
                        diff = time_diff_in_hours(in_t,shift_in)
                    if diff <= 2:
                        status = 'Present'
                    else:
                        status = 'Half Day'
                    frappe.errprint(diff)
                    frappe.errprint(status)
                elif pr.session == 'Second Half':
                    if pr.shift == '1':
                        shift_out = datetime.strptime('16:30', '%H:%M')
                        diff = time_diff_in_hours(shift_out,out_t)
                    elif pr.shift == '2':
                        shift_out = datetime.strptime('01:00', '%H:%M')
                        diff = time_diff_in_hours(shift_out,out_t)
                    elif pr.shift == '3':
                        shift_out = datetime.strptime('08:00', '%H:%M')
                        diff = time_diff_in_hours(shift_out,out_t)
                    elif pr.shift == 'PP1':
                        shift_out = datetime.strptime('20:00', '%H:%M')
                        diff = time_diff_in_hours(shift_out,out_t)
                    elif pr.shift == 'PP2':
                        shift_out = datetime.strptime('08:00', '%H:%M')
                        diff = time_diff_in_hours(shift_out,out_t)
                    if diff <= 2:
                        status = 'Present'
                    else:
                        status = 'Half Day'
                    frappe.errprint(diff)
                    frappe.errprint(status)
                att.status = status
                att.permission_request = pr.name
                att.save(ignore_permissions =True)
                att.submit()
                frappe.db.commit()
                if att.status in ('Half Day'):
                    from erpnext.hr.doctype.leave_application.leave_application import get_leave_details
                    leave_balance = get_leave_details(att.employee,nowdate())
                    leave_approver = component_amount = frappe.get_list("Department Approver",filters={'parent': att.department,'parentfield':"leave_approvers"},fields=["approver"])
                    if leave_approver:
                        lev_approver = leave_approver[0].approver
                    try:
                        if (leave_balance['leave_allocation']['Casual Leave']['remaining_leaves']) > 0:
                            leave_app = frappe.new_doc("Leave Application")
                            leave_app.employee = att.employee
                            leave_app.from_date = att.attendance_date
                            leave_app.to_date = att.attendance_date
                            leave_app.leave_type = 'Casual Leave'
                            leave_app.description = 'Auto-Leave for Exceeding Permission Hours'
                            leave_app.leave_approver = lev_approver
                            leave_app.save(ignore_permissions=True)
                            frappe.db.commit()
                        elif(leave_balance['leave_allocation']['Sick Leave']['remaining_leaves']) > 0:
                            l_app = frappe.new_doc("Leave Application")
                            l_app.employee = att.employee
                            l_app.from_date = att.attendance_date
                            l_app.to_date = att.attendance_date
                            l_app.leave_type = 'Sick Leave'
                            l_app.description = 'Auto-Leave for Exceeding Permission Hours'
                            l_app.leave_approver = lev_approver
                            l_app.save(ignore_permissions=True)
                            frappe.db.commit()
                        elif (leave_balance['leave_allocation']['Earned Leave']['remaining_leaves']) > 0:
                            lea_app = frappe.new_doc("Leave Application")
                            lea_app.employee = att.employee
                            lea_app.from_date = att.attendance_date
                            lea_app.to_date = att.attendance_date
                            lea_app.leave_type = 'Earned Leave'
                            lea_app.description = 'Auto-Leave for Exceeding Permission Hours'
                            lea_app.leave_approver = lev_approver
                            lea_app.save(ignore_permissions=True)
                            frappe.db.commit()           
                    except KeyError:
                        leave_balance['leave_allocation']['Casual Leave'] = 0
                        leave_balance['leave_allocation']['Sick Leave'] = 0
                        leave_balance['leave_allocation']['Earned Leave'] = 0