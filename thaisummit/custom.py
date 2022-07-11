from codecs import ignore_errors
from os import truncate
from types import FrameType
import frappe
import json
import datetime
from frappe import permissions
from frappe.utils.file_manager import get_file
from frappe.utils.csvutils import read_csv_content
from frappe.utils.data import format_date, get_url_to_list
from six.moves import range
from six import string_types
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
                          nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime, format_date)
from datetime import datetime
from calendar import IllegalMonthError, month, monthrange
from frappe import _, get_value, msgprint
from frappe.utils import flt, get_url_to_list
from frappe.utils import cstr, cint, getdate, get_first_day, get_last_day, today
import requests
from datetime import date, timedelta, time
import calendar
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
# from tabulate import tabulate
from datetime import datetime
import pandas as pd


def bulk_update_from_csv(filename):
    # below is the method to get file from Frappe File manager
    from frappe.utils.file_manager import get_file
    # Method to fetch file using get_doc and stored as _file
    _file = frappe.get_doc("File", {"file_name": filename})
    # Path in the system
    filepath = get_file(filename)
    # CSV Content stored as pps

    pps = read_csv_content(filepath[1])
    for pp in pps:
        date = "2021-02-28"
        print(pp[0])
        print(frappe.db.exists('Attendance', {
              'employee': pp[0], 'attendance_date': date}))
        for p in pp:
            if p != pp[0]:
                date = add_days(date, 1)
                if not frappe.db.exists('Attendance', {'attendance_date': date, 'employee': pp[0]}):
                    print(date, p)
                    status = ''
                    late = 0
                    if p in ['1', '2', '3', 'PP1', 'PP2', '1L', '2L', '3L', 'PP1L', 'PP2L']:
                        # print(p)
                        att = frappe.new_doc("Attendance")
                        att.employee = pp[0]
                        att.attendance_date = date
                        att.status = 'Present'
                        if p in ['1L', '2L', '3L', 'PP1L', 'PP2L']:
                            att.late_entry = 1
                            att.shift = p.strip('L')
                        else:
                            att.shift = p
                        att.save(ignore_permissions=True)
                        att.submit()
                        frappe.db.commit()
                    elif p in ['A', 'SL', 'EL', 'CL']:
                        att = frappe.new_doc("Attendance")
                        att.employee = pp[0]
                        att.attendance_date = date
                        att.status = 'Absent'
                        att.save(ignore_permissions=True)
                        att.submit()
                        frappe.db.commit()
                        # if p != 'A':
                        #     lev = frappe.new_doc("Leave Application")
                        #     lev.employee = pp[0]
                        #     lev.from_date = date
                        #     lev.to_date = date
                        #     lev.leave_approver = 'abdulla.pi@groupteampro.com'
                        #     lev.status = 'Approved'
                        #     if p == 'SL':
                        #         lev.leave_type = 'Sick Leave'
                        #     elif p == 'EL':
                        #         lev.leave_type = 'Earned Leave'
                        #     elif p == 'CL':
                        #         lev.leave_type = 'Casual Leave'
                        #     lev.save(ignore_permissions=True)
                        #     lev.submit()
                        #     frappe.db.commit()
                    elif p == 'OD':
                        od = frappe.new_doc("Attendance Request")
                        od.employee = pp[0]
                        od.from_date = date
                        od.to_date = date
                        od.reason = 'On Duty'
                        od.save(ignore_permissions=True)
                        od.submit()
                        frappe.db.commit()


def bulk_update_from_csv1(filename):
    # below is the method to get file from Frappe File manager
    from frappe.utils.file_manager import get_file
    # Method to fetch file using get_doc and stored as _file
    _file = frappe.get_doc("File", {"file_name": filename})
    # Path in the system
    filepath = get_file(filename)
    # CSV Content stored as pps

    pps = read_csv_content(filepath[1])
    for pp in pps:
        print(pp[0], pp[1])
        if frappe.db.exists('Employee', {'name': pp[0]}):
            doc = frappe.new_doc("QR Checkin")
            doc.employee = pp[0]
            doc.qr_shift = pp[2]
            doc.qr_scan_time = pp[1]
            doc.save(ignore_permissions=True)
            frappe.db.commit()
            att = frappe.db.exists(
                'Attendance', {'employee': pp[0], 'attendance_date': pp[1]})
            if att:
                print(pp[2])
                frappe.db.set_value('Attendance', att, 'qr_shift', pp[2])
                print(doc.name)
                frappe.db.set_value("QR Checkin", doc.name, 'attendance', att)


def qr_checkin_manual():
    emps = ["T0119",
            "VRV2102",
            "T1380",
            "T1589",
            "NT0346",
            "NT0143",
            "SRA0755",
            "SRA0758",
            "SRA1040",
            "ASR2194",
            "SRA0833",
            ]
    for emp in emps:
        doc = frappe.new_doc("QR Checkin")
        doc.employee = emp
        doc.employee_name = frappe.db.get_value(
            'Employee', emp, 'employee_name')
        doc.department = frappe.db.get_value('Employee', emp, 'department')
        doc.employee_type = frappe.db.get_value(
            'Employee', emp, 'employee_type')
        doc.qr_shift = '2'
        doc.qr_scan_time = '2022-03-20 16:30:00'
        doc.shift_date = '2022-03-20'
        doc.created_date = '2022-03-20'
        doc.save(ignore_permissions=True)
        frappe.db.commit()

# def update_leave_approver():
#     depts = frappe.get_all("Department")
#     for dep in depts:
#         if dep.name != 'All Departments':
#             doc = frappe.get_doc("Department",dep.name)
#             print(doc.name)
#             doc.append('leave_approvers',{
#                 'approver' : 'abdulla.pi@groupteampro.com'
#             })
#             doc.save(ignore_permissions=True)


def mail_wc_probation():
    employees = frappe.get_all("Employee", {"employment_type": "Probation", "employee_type": "WC"}, [
                               "date_of_joining", "name", "employee_name", "personal_email"])
    # print(employees)
    for emp in employees:
        # print(emp)
        t = relativedelta(months=5)
        fifth_month = emp.date_of_joining+t
        # print(fifth_month)
        s = relativedelta(months=6)
        sixth_month = emp.date_of_joining+s
        # print(sixth_month)
        today = datetime.today()
        if(fifth_month <= today.date() <= sixth_month):
            # print(emp.personal_email)
            frappe.sendmail(
                recipients=emp.personal_email,
                subject='Probation Period Date',
                message="""<p>Dear Admin,</p>
            <p> Probation period end date for  %s %s employee  </p>""" % (emp.name, emp.employee_name))


def mail_wc_get_trainee():
    employees = frappe.get_all("Employee", {"employment_type": "Trainee", "employee_type": "WC", "designation": "Graduate Engineer Trainee"}, [
                               "date_of_joining", "name", "employee_name", "personal_email"])
    # print(employees)
    for emp in employees:
        # print(emp)
        t = relativedelta(months=11)
        eleventh_month = emp.date_of_joining+t
        # print(eleventh_month)
        s = relativedelta(months=12)
        tewlth_month = emp.date_of_joining+s
        # print(tewlth_month)
        today = datetime.today()
        if(eleventh_month <= today.date() <= tewlth_month):
            # print("hi")
            frappe.sendmail(
                recipients=emp.personal_email,
                subject='Probation Period Date',
                message="""<p>Dear Admin,</p>
            <p> Trainee period end date for  %s %s employee  </p>""" % (emp.name, emp.employee_name))


def mail_wc_get_probation():
    employees = frappe.get_all("Employee", {"employment_type": "Probation", "employee_type": "WC", "designation": "Graduate Engineer Trainee"}, [
                               "date_of_joining", "name", "employee_name", "personal_email"])
    # print(employees)
    for emp in employees:
        # print(emp)
        t = relativedelta(months=17)
        eleventh_month = emp.date_of_joining+t
        # print(eleventh_month)
        s = relativedelta(months=18)
        tewlth_month = emp.date_of_joining+s
        # print(tewlth_month)
        today = datetime.today()
        if(eleventh_month <= today.date() <= tewlth_month):
            # print("hi")
            frappe.sendmail(
                recipients=emp.personal_email,
                subject='Probation Period Date',
                message="""<p>Dear Admin,</p>
            <p> Probation period end date for  %s %s employee  </p>""" % (emp.name, emp.employee_name))


def el_leave_policy():
    employees = frappe.get_all("Employee", {"employee_type": "WC"}, [
                               "name", "employee_name", "personal_email"])
    for emp in employees:
        print(emp.name)
        count = 0
        el = 0
        today = "2022-01-01"
        start_date = add_months(today, -12)
        end_date = add_days(today, -1)
        print(end_date)
        print(start_date)
        for att in (frappe.db.sql("""select status,attendance_date from `tabAttendance` where attendance_date between '%s' and '%s'  """ % (start_date, end_date), as_dict=True)):
            print(att)
            if (att.status == "Present"):
                count += 1
            else:
                count = 0
            # print(count)
            if count >= 20:
                el = count // 20 + el
                count = 0
                break
        print(el)
        print(datetime.today().date())
        get_la = frappe.new_doc("Leave Allocation")
        get_la.employee = emp.name
        get_la.leave_type = "Earned Leave"
        get_la.from_date = datetime.today().date()
        get_la.to_date = add_months(datetime.today().date(), 12)
        get_la.new_leaves_allocated = (int(el))
        get_la.save(ignore_permissions=True)
        frappe.db.commit()


def el_leave_encashment():
    employees = frappe.get_all("Employee", {"employee_type": "WC"}, ["name"])
    for emp in employees:
        print(emp.name)
        # if(emp.name == "TSAI0195"):
        get_le = frappe.new_doc("Leave Encashment")
        get_le.employee = emp.name
        get_le.leave_type = "Earned Leave"
        get_le.leave_period = "HR-LPR-2021-00001"
        get_le.save(ignore_permissions=True)
        frappe.db.commit()


@frappe.whitelist()
def create_user(employee_number, employee_name):
    # frappe.errprint(employee_number)
    user = frappe.new_doc("User")
    user.email = employee_number + "@gmail.com"
    user.first_name = employee_name
    user.username = employee_number
    user.send_welcome_mail = 0
    user.new_password = "thai@1234"
    user.save(ignore_permissions=True)
    frappe.db.commit()
    return user.email


@frappe.whitelist()
def get_sap_qty():
    parts = frappe.get_all('Part Master', ['mat_no', 'name'])
    url = "http://172.16.1.18/StockDetail/Service1.svc/GetFGQuantity"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers)
    frappe.errprint(response.status_code)
    if response.status_code == 200:
        for part in parts:
            url = "http://172.16.1.18/StockDetail/Service1.svc/GetFGQuantity"
            payload = json.dumps({
                "ItemCode": part['mat_no']
            })
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload)
            qty = json.loads(response.text)
            if qty:
                avl_qty = qty[0]['Qty']
                frappe.set_value(
                    "Part Master", part['name'], "sap_available_quantity", avl_qty)
                frappe.set_value(
                    "Part Master", part['name'], "sap_quantity_updated_on", datetime.now())
                frappe.set_value(
                    "Part Master", part['name'], "temp_avl_qty", avl_qty)
                frappe.set_value(
                    "Part Master", part['name'], "temp_qty_updated_on", datetime.now())
        return "Successfully Updated"
    else:
        return "Server Error"


@frappe.whitelist()
def deductions():
    last_mon = add_months(nowdate(), -1)
    today = nowdate()
    deduction = frappe.db.sql("""select employee, sum(amount) as total_amount from `tabDeductions` where docstatus=1 and
        MONTH(posting_date) = MONTH(%(mon)s) group by employee""", (dict(mon=last_mon)), as_dict=True)
    for ded in deduction:
        additional_salary = frappe.db.exists("Additional Salary", {
                                             "employee": ded.employee, "payroll_date": today, "salary_component": "Personal Protective Equipment", "docstatus": 1}, ["employee"])
        if not additional_salary:
            add_salary = frappe.new_doc("Additional Salary")
            add_salary.employee = ded.employee
            add_salary.salary_component = "Personal Protective Equipment"
            add_salary.amount = int(ded.total_amount)
            add_salary.payroll_date = nowdate()
            add_salary.overwrite_salary_structure_amount = "1"
            add_salary.save(ignore_permissions=True)
            add_salary.submit()
            frappe.db.commit()


@frappe.whitelist()
def change_leave_approver(employee, leave_approver):
    leave_application = frappe.db.get_all(
        "Leave Application", {"employee": employee, "docstatus": 0}, ["name"])
    for lev_app in leave_application:
        frappe.db.set_value('Leave Application', lev_app.name,
                            'leave_approver', leave_approver)


@frappe.whitelist()
def change_permission_approver(employee, permission_approver):
    permission_request = frappe.db.get_all(
        "Permission Request", {"employee": employee, "docstatus": 0}, ["name"])
    for per_req in permission_request:
        frappe.db.set_value('Permission Request', per_req.name,
                            'permission_approver', permission_approver)


@frappe.whitelist()
def change_od_approver(employee, od_approver):
    od_application = frappe.db.get_all(
        "On Duty Application", {"employee": employee, "docstatus": 0}, ["name"])
    for od_app in od_application:
        frappe.db.set_value('On Duty Application',
                            od_app.name, 'approver', od_approver)


# def employee_type():
#     emps = frappe.db.sql("select name from `tabEmployee` where name like 'V%' ")
#     print(len(emps))
#     for emp in emps:
#         print(emp[0])
#         frappe.db.set_value("Employee",emp[0],"vacant",1)


def is_weekoff(employee, date=None, raise_exception=True):
    '''Returns True if given Employee has a weekoff on the given date
    :param employee: Employee `name`
    :param date: Date to check. Will check for today if None'''

    holiday_list = get_holiday_list_for_employee(employee, raise_exception)
    if not date:
        date = today()
    if holiday_list:
        return frappe.get_all('Holiday List', dict(name=holiday_list, holiday_date=date, weekly_off=1)) and True or False


def is_holiday(employee, date=None, raise_exception=True):
    '''Returns True if given Employee has an holiday on the given date
    :param employee: Employee `name`
    :param date: Date to check. Will check for today if None'''

    holiday_list = get_holiday_list_for_employee(employee, raise_exception)
    if not date:
        date = today()
    if holiday_list:
        return frappe.get_all('Holiday List', dict(name=holiday_list, holiday_date=date,  weekly_off=0)) and True or False


def send_birthday_wish():
    birthdays = frappe.db.sql("""select name,date_of_birth,personal_email, employee_name
        from tabEmployee where day(date_of_birth) = day(%(date)s)
        and month(date_of_birth) = month(%(date)s)
        and status = 'Active'""", {"date": today()}, as_dict=True)
    print(birthdays)
    for emp in birthdays:
        print(emp.personal_email)
        if birthdays:
            frappe.sendmail(
                recipients=emp.personal_email,
                subject="Birthday Wishes",
                message="""<p> Dear %s <br> May your birthday be the start of a year filled with good luck, good health and much happiness, <br>
            We wish you an amazing year that ends with accomplishing all the great goals that you have set!</p>""" % (emp.employee_name))


@frappe.whitelist()
def send_confirmation_mail(employee_number, employee_name, personal_email, confirmation_message):
    frappe.sendmail(
        recipients=personal_email,
        subject="Birthday Wishes",
        message="""<p> Dear %s <br>
    %s
    </p>""" % (employee_name, confirmation_message))


@frappe.whitelist()
def get_shift(emp):
    previous_month = frappe.utils.add_months(
        datetime.today(), -1).strftime("%Y-%m-26")
    current_month = (datetime.today()).strftime("%Y-%m-25")
    date_list = get_dates(previous_month, current_month)
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
        if frappe.db.exists('Attendance', {'employee': emp, 'attendance_date': date, 'docstatus': ['!=', '2']}):
            att = frappe.get_doc('Attendance', {
                                 'employee': emp, 'attendance_date': date, 'docstatus': ['!=', '2']})
            # if rd1 == str(A):
            #     """<td style='color:red'> A </td>  """
            # frappe.errprint(date)
            frappe.errprint(att.shift)
            if i <= 10:
                rh1 += """<th><center>%s</center></th>""" % (
                    (datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                rd1 += """<td><center>%s</center></td>""" % (att.shift or 'A')
                if i == 10:
                    r1 = rh1 + '</tr>' + rd1 + '</tr>'
            elif 10 < i <= 20:
                rh2 += """<th><center>%s</center></th>""" % (
                    (datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                rd2 += """<td><center>%s</center></td>""" % (att.shift or 'A')
                if i == 20:
                    r2 = '<tr>' + rh2 + '</tr><tr>' + rd2 + '</tr>'
            elif 20 < i:
                rh3 += """<th><center>%s</center></th>""" % (
                    (datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                rd3 += """<td><center>%s</center></td>""" % (att.shift or 'A')
            i += 1
        data = "<table border='1' class='table table-bordered'>" + r1 + \
            r2 + '<tr>' + rh3 + '</tr><tr>' + rd3 + '</tr>' + "</table>"
    return data


def get_dates(previous_month, current_month):
    """get list of date s in between from date and to date"""
    no_of_days = date_diff(add_days(current_month, 1), previous_month)
    dates = [add_days(previous_month, i) for i in range(0, no_of_days)]
    return dates


def send_mail_hr():
    """Continous absent employees for 5 days mail sent to hr """
    current_date = (datetime.today()).strftime("%Y-%m-%d")
    five_days = frappe.utils.add_days(
        datetime.today(), -5).strftime("%Y-%m-%d")
    print(five_days)
    print(current_date)
    get_att = frappe.db.sql(""" select employee_name,employee,count(status) as absent_count from `tabAttendance` where status ='Absent' and docstatus = '1' and attendance_date between '%s' and '%s'  group by employee""" % (
        five_days, current_date), as_dict=True)
    print(get_att)
    data = ''
    header = """<tr> <th>SL No </th> <th> Employee ID</th><th> Employee Name </tr>"""
    for idx, att in enumerate(get_att):
        if att.absent_count == 5:
            data += """ <tr> <td> %s </td> <td> %s </td> <td> %s </td> </tr>""" % (
                idx+1, att.employee, att.employee_name)
    data = "<table border='1' class='table table-bordered'>" + header + data + "</table>"
    frappe.sendmail(
        recipients=['sarumathy.d@groupteampro.com'],
        subject="Absent Employees",
        message=data)


def create_leave_allocation():
    # current_date = (datetime.today()).strftime("%Y-%m-%d")
    three_days = frappe.utils.add_days(
        datetime.today(), -3).strftime("%Y-%m-%d")
    print(three_days)
    employees = frappe.get_all("Employee", {"status": "Active"}, [
                               "name", "employee_name", "personal_email"])
    for emp in employees:
        # print(emp.name)
        attendance = frappe.db.get_all('Attendance', {
                                       'employee': emp.name, 'attendance_date': three_days, 'docstatus': '1'}, ["status", "employee"])
        for att in attendance:
            # print(att.status)
            if att.status in ('Half Day'):
                from erpnext.hr.doctype.leave_application.leave_application import get_leave_details
                leave_balance = get_leave_details(att.employee, nowdate())
                try:
                    if (leave_balance['leave_allocation']['Casual Leave']['remaining_leaves']) > 0:
                        leave_app = frappe.new_doc("Leave Application")
                        leave_app.employee = att.employee
                        leave_app.from_date = three_days
                        leave_app.to_date = three_days
                        leave_app.leave_type = 'Casual Leave'
                        leave_app.description = 'Auto-Leave Application for Late In Entry'
                        leave_app.leave_approver = "Administrator"
                        leave_app.save(ignore_permissions=True)
                        frappe.db.commit()

                    elif(leave_balance['leave_allocation']['Sick Leave']['remaining_leaves']) > 0:
                        l_app = frappe.new_doc("Leave Application")
                        l_app.employee = att.employee
                        l_app.from_date = three_days
                        l_app.to_date = three_days
                        l_app.leave_type = 'Sick Leave'
                        l_app.description = 'Auto-Leave Application for Late In Entry'
                        l_app.leave_approver = "Administrator"
                        l_app.save(ignore_permissions=True)
                        frappe.db.commit()
                    elif (leave_balance['leave_allocation']['Earned Leave']['remaining_leaves']) > 0:
                        lea_app = frappe.new_doc("Leave Application")
                        lea_app.employee = att.employee
                        lea_app.from_date = three_days
                        lea_app.to_date = three_days
                        lea_app.leave_type = 'Earned Leave'
                        lea_app.description = 'Auto-Leave Application for Late In Entry'
                        lea_app.leave_approver = "Administrator"
                        lea_app.save(ignore_permissions=True)
                        frappe.db.commit()
                except KeyError:
                    leave_balance['leave_allocation']['Casual Leave'] = 0
                    leave_balance['leave_allocation']['Sick Leave'] = 0
                    leave_balance['leave_allocation']['Earned Leave'] = 0


def add_special_leave():
    lle = frappe.new_doc("Leave Ledger Entry")
    lle.employee = "5"
    lle.from_date = '2021-01-01'
    lle.to_date = '2021-12-31'
    lle.leave_type = 'Casual Leave'
    lle.transaction_type = 'Leave Allocation'
    lle.leaves = "10"
    lle.save(ignore_permissions=True)
    lle.submit()
    frappe.db.commit()


@frappe.whitelist()
def exceed_vehicle_load(name, vehicle_name):
    emp = frappe.db.count('Employee', {'vehicle_name': vehicle_name})
    load = frappe.db.get_value("Vehicle Management", {
                               'name': vehicle_name}, ['load_capacity'])
    balance_load = int(load - emp)
    # frappe.errprint(balance_load)
    # if(emp >= load):
    #     return "Vehicle Load Exceeded"
    return emp, load


@frappe.whitelist()
def delete_shift_summary():
    ss = frappe.get_all("Shift Schedule Status Summary")
    for s in ss:
        doc = frappe.get_doc("Shift Schedule Status Summary", s.name)
        doc.delete()


@frappe.whitelist()
def mark_qr_user(user, status):
    user = frappe.get_doc('User', user)
    if status == 'Add':
        user.role_profile_name = ''
        user.add_roles('QR User')
        frappe.errprint('add')
    else:
        user.remove_roles('QR User')
        frappe.errprint('remove')
    user.save(ignore_permissions=True)


@frappe.whitelist()
def mark_qr_user_from_csv(filename):
    # below is the method to get file from Frappe File manager
    from frappe.utils.file_manager import get_file
    # Method to fetch file using get_doc and stored as _file
    _file = frappe.get_doc("File", {"file_name": filename})
    # Path in the system
    filepath = get_file(filename)
    # CSV Content stored as pps
    pps = read_csv_content(filepath[1])
    for pp in pps:
        # print(pp[0])
        userid = frappe.get_value('Employee', pp[0], 'user_id')
        username = frappe.db.exists('User', userid)
        if username:
            user = frappe.get_doc('User', username)
            user.role_profile_name = ''
            user.add_roles('QR User')
            user.save(ignore_permissions=True)

# def update_qr():
#     qrs = frappe.get_all("QR Checkin",{'shift_date':'2021-05-05'},["shift_date","qr_shift","employee"])
#     for qr in qrs:
#         att = frappe.db.exists("Attendance",{'employee':qr.employee,'attendance_date':qr.shift_date})
#         print(att)
#         frappe.db.set_value("Attendance",att,"qr_shift",qr.qr_shift)
#         frappe.db.set_value("Attendance",att,"qr_scan_time",qr.qr_scan_time)


@frappe.whitelist()
def roundoff_time(time):
    time = datetime.strptime(time, '%H:%M:%S')
    if time.minute not in (0, 30):
        if time.minute < 30:
            roundoff_time = time.replace(minute=0)
        elif time.minute >= 30:
            roundoff_time = time.replace(minute=30)
        roundoff_time = roundoff_time.time()
        return str(roundoff_time)


@frappe.whitelist()
def get_employee_code(user):
    emp_id = frappe.db.get_value('Employee', {'user_id': user}, "name")
    return emp_id

# @frappe.whitelist()
# def get_ceo(department):
#     ceo = frappe.db.get_value('Department',department,"ceo")
#     return ceo

# @frappe.whitelist()
# def get_gm(department):
#     gm = frappe.db.get_value('Department',department,"gm")
#     return gm


@frappe.whitelist()
def get_approver(department, employee):
    user = frappe.db.get_value('Employee', employee, 'user_id')
    roles = frappe.get_roles(user)
    if 'GM' in roles:
        return frappe.db.get_value('Department', department, "ceo")
    elif 'HOD' in roles:
        return frappe.db.get_value('Department', department, "gm")
    else:
        return frappe.db.get_value('Department', department, "hod")


@frappe.whitelist()
def update_user_permission(user, department):
    if not frappe.db.exists("User Permission", {'user': user, 'allow': "Department", "for_value": department, "is_default": 1}):
        default = frappe.db.exists(
            "User Permission", {'user': user, 'allow': "Department", "is_default": '1'})
        if default:
            frappe.delete_doc("User Permission", default)
        up = frappe.db.exists("User Permission", {
                              'user': user, 'allow': "Department", 'for_value': department})
        if up:
            doc = frappe.get_doc("User Permission", up)
            doc.is_default = 1
            doc.save(ignore_permissions=True)
        else:
            doc = frappe.new_doc("User Permission")
            doc.user = user
            doc.allow = "Department"
            doc.for_value = department
            doc.is_default = 1
            doc.save(ignore_permissions=True)


@frappe.whitelist()
def check_leave_balance(employee, leave_type):
    from erpnext.hr.doctype.leave_application.leave_application import get_leave_details
    leave_balance = get_leave_details(employee, nowdate())
    if leave_type not in ('Special Leave', 'Compensatory Off', 'Leave Without Pay'):
        balance = leave_balance['leave_allocation'][leave_type]['remaining_leaves']
        la = frappe.db.count('Leave Application', {
                             'employee': employee, 'docstatus': 0})
        if la > balance:
            frappe.throw(
                'There is not enough leave balance for Leave Type %s' % (leave_type))


@frappe.whitelist()
def application_allowed_from(date):
    # date = datetime.strptime(date, '%Y-%m-%d').date()
    # today_date = datetime.strptime('2021-07-29', '%Y-%m-%d').date()
    # # today_date = datetime.strptime(today(), '%Y-%m-%d').date()
    # if today_date.day <= 28:
    #     last_month = add_months(today_date,-1)
    #     last_month_start = get_first_day(last_month)
    #     allowed_from = add_days(last_month_start,25)
    #     cur_month_start = get_last_day(today_date)
    #     allowed_till = add_days(cur_month_start,25)
    #     frappe.errprint(allowed_from)
    #     frappe.errprint(allowed_till)
    #     if date < allowed_from:
    #         frappe.msgprint('Application not allowed before %s'%allowed_from)
    #         return 'NO'
    #     if date > allowed_till:
    #         frappe.msgprint('Application not allowed after %s'%allowed_till)
    #         return 'NO'
    # else:
    #     cur_month_start = get_first_day(today_date)
    #     allowed_from = add_days(cur_month_start,25)
    #     month_end = get_last_day(cur_month_start)
    #     allowed_till = add_days,(month_end,25)
    #     frappe.errprint(allowed_from)
    #     frappe.errprint(allowed_till)
    #     if date < allowed_from:
    #         frappe.msgprint('Application not allowed before %s'%allowed_from)
    #         return 'NO'
    #     if date > allowed_till:
    #         frappe.msgprint('Application not allowed after %s'%allowed_till)
    #         return 'NO'
    return ''

# @frappe.whitelist()
# def update_dept():
#     employess = frappe.get_all('Employee',['department','user_id','name'])
#     for emp in employess:
#         print(emp.name)
#         if frappe.db.exists('User Permission',{'user':emp.user_id,'allow':'Department','for_value':emp.department}):
#             doc = frappe.get_doc('User Permission',{'user':emp.user_id,'allow':'Department','for_value':emp.department})
#             doc.is_default = 1
#             doc.save(ignore_permissions=True)


# def delete_dept():
#     atts = frappe.get_all('Attendance',{'Department':'TLS Dept'})
#     print(len(atts))
#     for att in atts:
#         ec = frappe.get_all('Employee Checkin',{'attendance':att.name})
#         frappe.delete_doc("Attendance",att.name)
#         # if ec:
#         #     print(ec[0])
#         #     frappe.delete_doc("Employee Checkin",ec[0].name)

# def delete_shift():
#     from_date = '2021-06-26'
#     sa_list = frappe.db.sql("select name from `tabShift Assignment` where start_date = '%s' and docstatus = 1 "%(from_date),as_dict=True)
#     if sa_list:
#         for sa in sa_list:
# @frappe.whitelist()
# def mark_att(from_date,to_date):
#     checkins = frappe.db.sql(
#         """select * from `tabEmployee Checkin` where skip_auto_attendance = 0 and date(time) between '%s' and '%s' """%(from_date,to_date),as_dict=1)
#     if checkins:
#         for c in checkins:
#             att = mark_attendance_from_checkin(c.name,c.employee,c.log_type,c.time)
#             # print(att)
#             if att:
#                 frappe.db.set_value("Employee Checkin",
#                                     c.name, "skip_auto_attendance", "1")
#         frappe.msgprint("Attendance Marked Successfully")
#         return "ok"
#     else:
#         frappe.msgprint("Attendance Already Marked")

# def mark_attendance_from_checkin(checkin,employee,log_type,time):
#     att_time = time.time()
#     att_date = time.date()
#     month_start_date = get_first_day(att_date)
#     month_end_date = get_last_day(att_date)
#     shift = ''
#     if log_type == 'IN':
#         min_in_time = ''
#         max_in_time = ''
#         min_in_time1 = datetime.strptime('06:00', '%H:%M').time()
#         max_in_time1 = datetime.strptime('10:00', '%H:%M').time()
#         min_in_time2 = datetime.strptime('14:30', '%H:%M').time()
#         max_in_time2 = datetime.strptime('18:30', '%H:%M').time()
#         min_in_time3 = datetime.strptime('00:01', '%H:%M').time()
#         max_in_time3 = datetime.strptime('03:00', '%H:%M').time()
#         min_in_timepp1 = datetime.strptime('06:00', '%H:%M').time()
#         max_in_timepp1 = datetime.strptime('10:00', '%H:%M').time()
#         min_in_timepp2 = datetime.strptime('18:00', '%H:%M').time()
#         max_in_timepp2 = datetime.strptime('22:00', '%H:%M').time()
#         late1 = datetime.strptime('08:10', '%H:%M').time()
#         late2 = datetime.strptime('16:40', '%H:%M').time()
#         late3 = datetime.strptime('01:10', '%H:%M').time()
#         latepp1 = datetime.strptime('08:10', '%H:%M').time()
#         latepp2 = datetime.strptime('20:10', '%H:%M').time()
#         late = 0
#         status = 'Present'
#         if max_in_time1 >= att_time >= min_in_time1:
#             if frappe.db.get_value('Employee',employee,"default_shift") == 'PP1':
#                 shift = 'PP1'
#             else:
#                 shift = '1'
#             min_in_time = datetime.strptime('07:00', '%H:%M').time()
#             max_in_time = datetime.strptime('09:00', '%H:%M').time()
#             if datetime.strptime('08:00', '%H:%M').time() <= att_time <= datetime.strptime('08:10', '%H:%M').time():
#                 late = 1
#             elif att_time > datetime.strptime('08:00', '%H:%M').time():
#                 status = 'Half Day'
#         elif max_in_time2 >= att_time >= min_in_time2:
#             shift = '2'
#             min_in_time = datetime.strptime('15:30', '%H:%M').time()
#             max_in_time = datetime.strptime('17:30', '%H:%M').time()
#             if datetime.strptime('16:30', '%H:%M').time() <= att_time <= datetime.strptime('16:40', '%H:%M').time():
#                 late = 1
#             elif att_time > datetime.strptime('16:30', '%H:%M').time():
#                 status = 'Half Day'
#         elif max_in_time3 >= att_time >= min_in_time3:
#             shift = '3'
#             att_date = add_days(att_date,-1)
#             min_in_time = datetime.strptime('00:01', '%H:%M').time()
#             max_in_time = datetime.strptime('02:00', '%H:%M').time()
#             if datetime.strptime('01:00', '%H:%M').time() <= att_time <= datetime.strptime('01:10', '%H:%M').time():
#                 late = 1
#             elif att_time > datetime.strptime('01:00', '%H:%M').time():
#                 status = 'Half Day'
#         elif max_in_timepp2 >= att_time >= min_in_timepp2:
#             shift = 'PP2'
#             min_in_time = datetime.strptime('19:00', '%H:%M').time()
#             max_in_time = datetime.strptime('21:00', '%H:%M').time()
#             if datetime.strptime('20:00', '%H:%M').time() <= att_time <= datetime.strptime('20:10', '%H:%M').time():
#                 late = 1
#             elif att_time > datetime.strptime('20:00', '%H:%M').time():
#                 status = 'Half Day'
#         if late == 1:
#             count = frappe.db.sql("select count(*) as count from `tabAttendance` where employee = '%s' and docstatus != 2 and late_entry =1 and attendance_date between '%s' and '%s' "%(employee,month_start_date,month_end_date),as_dict = True)
#             if count[0].count:
#                 if int(count[0].count) >= 2:
#                     status = 'Half Day'
#         if min_in_time and max_in_time:
#             if not frappe.db.exists("Attendance",{'employee':employee,'attendance_date':att_date,'docstatus': ['!=',2]}):
#                 if shift != '3':
#                     checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s' order by time "%(employee,att_date,min_in_time,max_in_time),as_dict=True)
#                 else:
#                     yesterday = add_days(att_date,1)
#                     checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s' order by time "%(employee,yesterday,min_in_time,max_in_time),as_dict=True)
#                 if checkins:
#                     qr_checkin = frappe.db.sql("select name, employee,qr_shift,qr_scan_time,shift_date from `tabQR Checkin` where employee = '%s' and date(qr_scan_time) = '%s' order by qr_scan_time "%(employee,att_date),as_dict=True)
#                     att = frappe.new_doc("Attendance")
#                     att.employee = employee
#                     att.attendance_date = att_date
#                     att.shift = shift
#                     att.status = status
#                     att.late_entry = late
#                     att.in_time = checkins[0].time
#                     if qr_checkin:
#                         att.qr_shift = qr_checkin[0].qr_shift
#                         att.qr_scan_time = qr_checkin[0].qr_scan_time
#                     att.save(ignore_permissions=True)
#                     frappe.db.commit()
#                     frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
#                     if qr_checkin:
#                         frappe.db.set_value("QR Checkin",qr_checkin[0].name, "attendance", att.name)
#                     return att
#     if log_type == 'OUT':
#         max_out = datetime.strptime('10:00', '%H:%M').time()
#         if att_time < max_out:
#             yesterday = add_days(att_date,-1)
#             checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'OUT' and date(time) = '%s' and time(time) < '%s' order by time "%(employee,att_date,max_out),as_dict=True)
#             att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':yesterday})
#             frappe.errprint(att)
#             if att:
#                 att = frappe.get_doc("Attendance",att)
#                 print(att.name)
#                 if not att.out_time:
#                     if att.docstatus == 0:
#                         print(att.out_time)
#                         if len(checkins) > 0:
#                             att.out_time = checkins[-1].time
#                         else:
#                             att.out_time = checkins[0].time
#                         att.save(ignore_permissions=True)
#                         att.submit()
#                         frappe.db.commit()
#                         frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
#                         return att
#             else:
#                 att = frappe.new_doc("Attendance")
#                 att.employee = employee
#                 att.attendance_date = yesterday
#                 # att.shift_type = shift
#                 att.status = 'Absent'
#                 if len(checkins) > 0:
#                     att.out_time = checkins[-1].time
#                 else:
#                     att.out_time = checkins[0].time
#                 att.save(ignore_permissions=True)
#                 frappe.db.commit()
#                 frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
#                 return att
#         else:
#             checkins = frappe.db.sql("select name,time,docstatus from `tabEmployee Checkin` where employee ='%s' and log_type = 'OUT' and date(time) = '%s' order by time "%(employee,att_date),as_dict=True)
#             att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':att_date})
#             if att:
#                 att = frappe.get_doc("Attendance",att)
#                 if not att.out_time:
#                     if att.docstatus == 0:
#                         if len(checkins) > 0:
#                             att.out_time = checkins[-1].time
#                         else:
#                             att.out_time = checkins[0].time
#                         att.save(ignore_permissions=True)
#                         att.submit()
#                         frappe.db.commit()
#                         frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
#                         return att
#             else:
#                 att = frappe.new_doc("Attendance")
#                 att.employee = employee
#                 att.attendance_date = att_date
#                 # att.shift_type = shift
#                 att.status = 'Absent'
#                 if len(checkins) > 0:
#                     att.out_time = checkins[-1].time
#                 else:
#                     att.out_time = checkins[0].time
#                 att.save(ignore_permissions=True)
#                 frappe.db.commit()
#                 frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
#                 return att


# def mark_attendance_from_checkin(checkin,employee,log_type,time):
#     att_time = time.time()
#     att_date = time.date()
#     if log_type == 'IN':
# new_doc("Attendance")
    #             attendance.update({
    #                 "employee": employee,
    #                 "status": status,
    #                 "attendance_date":log_date,
    #                 "plant":plant,
    #                 "in": att_time,
    #                 "out":"",
    #                 "total_working_hours":"",
    #                 "extra_hours":"",
    #                 "approved_ot_hours":"",
    #                 "shift": shift
    #             })
    #             attendance.save(ignore_permissions=True)
    #             frappe.db.set_value("Employee Checkin",checkin,"attendance",attendance.name)
    #             frappe.db.commit()
    #             return "ok"
#             doc = frappe.get_doc("Shift Assignment",sa.name)
#             doc.cancel()
#         frappe.msgprint('Shift Schedule Deleted Successfully')
#     else:
#         frappe.msgprint('No Shift Schedule found')

# def bulk_ot():
#     emps = frappe.get_all("Employee",{'employee_type':"WC"},['name','user_id'])
#     for emp in emps:
#         if emp.user_id:
#             user = frappe.get_doc('User',emp.user_id)
#             user.add_roles('Bulk OT')
#             user.save(ignore_permissions=True)

# def method(filename):
#     from frappe.utils.file_manager import get_file
#     filepath = get_file(filename)
#     pps = read_csv_content(filepath[1])
#     for pp in pps:
#         print(pp[0])
#         frappe.delete_doc('QR Checkin',pp[0])

# def method():
#     # doc = frappe.get_doc('Leave Application','HR-LAP-2021-00962')
#     # doc.cancel()
#     frappe.delete_doc('Leave Application','HR-LAP-2021-00962')
#     # frappe.db.set_value('Attendance','HR-ATT-2021-165365','status','Half Day')

def bulk_mail_alerts():
    dept = frappe.get_all('Department', {'is_group': '0'})
    header = """<p>Dear sir, <br> Please find the below list of Application pending for your Approval.</p><table class='table table-bordered'> """
    link = get_url_to_list("Approval")
    view = "<table><tr><th style = 'border: 1px solid black;background-color:#ffedcc;'><center><a href='%s'>View Approval Summary</a></center></th></tr></table><br>" % (
        link)
    regards = "Thanks & Regards,<br>hrPRO"
    for d in dept:
        hod = frappe.db.get_value('Department', d.name, "hod")
        content = ''
        ots = ''
        miss_punch = ''
        leave_application = ''
        ots = frappe.get_all("Overtime Request", {"department": d.name, "workflow_state": "Pending for HOD"}, [
                             'employee', 'employee_name', 'ot_date', 'ot_hours'])
        if ots:
            content += """<table><tr><th style = 'border: 1px solid black;background-color:#ffedcc;' colspan = "5" ><center>Overtime Request</center></th></tr><tr><th style = 'border: 1px solid black'>Department</th><th style = 'border: 1px solid black'>Employee ID</th><th style = 'border: 1px solid black'>Employee Name</th><th style = 'border: 1px solid black'>OT Date</th><th style = 'border: 1px solid black'>OT Hour</th></tr>"""
            for ot in ots:
                content += '<tr><td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td> <td style = "border: 1px solid black"> %s </td> <td style = "border: 1px solid black"> %s </td></tr>' % (
                    d['name'], ot['employee'], ot['employee_name'], format_date(ot['ot_date']), ot['ot_hours'])
            content += '</table><br>'

        miss_punch = frappe.get_all("Miss Punch Application", {"department": d.name, "workflow_state": "Pending for HOD"}, [
                                    'employee', 'employee_name', 'in_time', 'out_time', 'attendance_date'])
        if miss_punch:
            content += """<table class='table table-bordered'><tr><th style = 'border: 1px solid black;background-color:#ffedcc;' colspan = "6"><center>Manual Attendance Correction</center></th></tr><tr><th style = 'border: 1px solid black'>Department</th><th style = 'border: 1px solid black'>Employee ID</th><th style = 'border: 1px solid black'>Employee Name</th><th style = 'border: 1px solid black'>Date</th><th style = 'border: 1px solid black'>IN Time</th><th style = 'border: 1px solid black'>OUT Time</th></tr>"""
            for mp in miss_punch:
                content += '<tr><td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td> <td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td> <td style = "border: 1px solid black"> %s </td></tr>' % (
                    d['name'], mp.employee, mp.employee_name, mp.attendance_date, format_datetime(mp.in_time), format_datetime(mp.out_time))
            content += '</table><br>'

        leave_application = frappe.get_all("Leave Application", {
                                           "department": d.name, "workflow_state": "Pending for HOD"}, ['*'])
        if leave_application:
            content += """<table class='table table-bordered'><tr><th colspan = "8" style = 'border: 1px solid black;background-color:#ffedcc;'><center>Leave Application</center></th></tr><tr><th style = 'border: 1px solid black'>Department</th><th style = 'border: 1px solid black'>Employee ID</th><th style = 'border: 1px solid black'>Employee Name</th><th style = 'border: 1px solid black'>From Date</th><th style = 'border: 1px solid black'>To Date</th><th style = 'border: 1px solid black'>Leave Type</th><th style = 'border: 1px solid black'>Session</th><th style = 'border: 1px solid black'>Reason</th></tr>"""
            for leave in leave_application:
                content += '<tr><td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td> <td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td> <td style = "border: 1px solid black"> %s </td> <td style = "border: 1px solid black"> %s </td></tr>' % (
                    d['name'], leave.employee, leave.employee_name, format_date(leave.from_date), format_date(leave.to_date), leave.leave_type, leave.session, leave.description)
            content += '</table><br>'

        if ots or miss_punch or leave_application:
            print(d.name)
            if hod:
                frappe.sendmail(
                    recipients=[hod, 'mohan.pan@thaisummit.co.in'],
                    subject='Reg.List of pending Approvals',
                    message=header+content+view+regards)


@frappe.whitelist()
def update_approver(dept, hod, gm, ceo):
    ots = frappe.db.get_all("Overtime Request", {
                            "department": dept, "docstatus": 0}, ["name", "employee"])
    for ot in ots:
        user = frappe.db.get_value('Employee', ot.employee, 'user_id')
        roles = frappe.get_roles(user)
        if 'GM' in roles:
            approver_id = frappe.db.get_value("User", ceo, 'username')
            approver_name = frappe.db.get_value("User", ceo, 'full_name')
            frappe.db.set_value('Overtime Request', ot.name, 'approver', ceo)
            frappe.db.set_value('Overtime Request', ot.name,
                                'approver_id', approver_id)
            frappe.db.set_value('Overtime Request', ot.name,
                                'approver_name', approver_name)

        elif 'HOD' in roles:
            approver_id = frappe.db.get_value("User", gm, 'username')
            approver_name = frappe.db.get_value("User", gm, 'full_name')
            frappe.db.set_value('Overtime Request', ot.name, 'approver', gm)
            frappe.db.set_value('Overtime Request', ot.name,
                                'approver_id', approver_id)
            frappe.db.set_value('Overtime Request', ot.name,
                                'approver_name', approver_name)
        else:
            approver_id = frappe.db.get_value("User", hod, 'username')
            approver_name = frappe.db.get_value("User", hod, 'full_name')
            frappe.db.set_value('Overtime Request', ot.name, 'approver', hod)
            frappe.db.set_value('Overtime Request', ot.name,
                                'approver_id', approver_id)
            frappe.db.set_value('Overtime Request', ot.name,
                                'approver_name', approver_name)

    leave_apps = frappe.db.get_all("Leave Application", {
                                   "department": dept, "docstatus": 0}, ["name", "employee"])
    for la in leave_apps:
        user = frappe.db.get_value('Employee', la.employee, 'user_id')
        roles = frappe.get_roles(user)
        if 'GM' in roles:
            approver_name = frappe.db.get_value("User", ceo, 'full_name')
            frappe.db.set_value('Leave Application',
                                la.name, 'leave_approver', ceo)
            frappe.db.set_value('Leave Application', la.name,
                                'leave_approver_name', approver_name)

        elif 'HOD' in roles:
            approver_name = frappe.db.get_value("User", gm, 'full_name')
            frappe.db.set_value('Leave Application',
                                la.name, 'leave_approver', gm)
            frappe.db.set_value('Leave Application', la.name,
                                'leave_approver_name', approver_name)
        else:
            approver_name = frappe.db.get_value("User", hod, 'full_name')
            frappe.db.set_value('Leave Application',
                                la.name, 'leave_approver', hod)
            frappe.db.set_value('Leave Application', la.name,
                                'leave_approver_name', approver_name)

    permissions = frappe.db.get_all("Permission Request", {
                                    "department": dept, "docstatus": 0}, ["name", "employee"])
    for p in permissions:
        user = frappe.db.get_value('Employee', p.employee, 'user_id')
        roles = frappe.get_roles(user)
        if 'GM' in roles:
            approver_name = frappe.db.get_value("User", ceo, 'full_name')
            frappe.db.set_value('Permission Request', p.name,
                                'permission_approver', ceo)
            frappe.db.set_value('Permission Request', p.name,
                                'permission_approver_name', approver_name)

        elif 'HOD' in roles:
            approver_name = frappe.db.get_value("User", gm, 'full_name')
            frappe.db.set_value('Permission Request', p.name,
                                'permission_approver', gm)
            frappe.db.set_value('Permission Request', p.name,
                                'permission_approver_name', approver_name)
        else:
            approver_name = frappe.db.get_value("User", hod, 'full_name')
            frappe.db.set_value('Permission Request', p.name,
                                'permission_approver', hod)
            frappe.db.set_value('Permission Request', p.name,
                                'permission_approver_name', approver_name)

    ods = frappe.db.get_all("On Duty Application", {
                            "department": dept, "docstatus": 0}, ["name", "employee"])
    for od in ods:
        user = frappe.db.get_value('Employee', od.employee, 'user_id')
        roles = frappe.get_roles(user)
        if 'GM' in roles:
            approver_name = frappe.db.get_value("User", ceo, 'full_name')
            frappe.db.set_value('On Duty Application',
                                od.name, 'approver', ceo)
            frappe.db.set_value('On Duty Application', od.name,
                                'approver_name', approver_name)

        elif 'HOD' in roles:
            approver_name = frappe.db.get_value("User", gm, 'full_name')
            frappe.db.set_value('On Duty Application', od.name, 'approver', gm)
            frappe.db.set_value('On Duty Application', od.name,
                                'approver_name', approver_name)
        else:
            approver_name = frappe.db.get_value("User", hod, 'full_name')
            frappe.db.set_value('On Duty Application',
                                od.name, 'approver', hod)
            frappe.db.set_value('On Duty Application', od.name,
                                'approver_name', approver_name)
    return 'ok'


@frappe.whitelist()
def check_qr(from_date, to_date, employee):
    emp_type = frappe.db.get_value("Employee", employee, 'employee_type')
    if emp_type != 'WC':
        qr = frappe.db.sql("select name from `tabQR Checkin` where employee = '%s' and shift_date between '%s' and '%s' " % (
            employee, from_date, to_date), as_dict=True)
        if qr:
            return qr


# @frappe.whitelist()
# def change_permission_approver(employee,permission_approver):
#     permission_request = frappe.db.get_all("Permission Request",{"employee":employee,"docstatus":0},["name"])
#     for per_req in permission_request:
#         frappe.db.set_value('Permission Request',per_req.name,'permission_approver',permission_approver)

# @frappe.whitelist()
# def change_od_approver(employee,od_approver):
#     od_application = frappe.db.get_all("On Duty Application",{"employee":employee,"docstatus":0},["name"])
#     for od_app in od_application:
#         frappe.db.set_value('On Duty Application',od_app.name,'approver',od_approver)

# def update():
#     frappe.db.set_value('E','EMP-CKIN-07-2021-064271','attendance','')

# def get_la():
#     frappe.db.set_value('Attendance','HR-ATT-2021-217554','leave_type','Earned Leave')
#     a = frappe.db.set_value('Attendance','HR-ATT-2021-217554','leave_application','HR-LAP-2021-01557')

def create_ss():
    emps = frappe.get_all('Employee', {'status': 'Active'}, ['*'])
    for emp in emps:
        structure = ''
        if not frappe.db.exists('Salary Structure Assignment', {'employee': emp.name}):
            if emp.employee_type == 'WC':
                structure = 'WC'
            elif emp.employee_type == 'BC':
                structure = 'BC Salary Structure'
            elif emp.employee_type == 'CL':
                structure = 'CL Structure'
            if structure:
                try:
                    doc = frappe.new_doc('Salary Structure Assignment')
                    doc.employee = emp.name
                    doc.salary_structure = structure
                    doc.from_date = '2021-07-24'
                    doc.save(ignore_permissions=True)
                    doc.submit()
                    frappe.db.commit()
                except:
                    doc = frappe.new_doc('Salary Structure Assignment')
                    doc.employee = emp.name
                    doc.salary_structure = structure
                    doc.from_date = frappe.db.get_value(
                        'Employee', emp.name, 'date_of_joining')
                    doc.save(ignore_permissions=True)
                    doc.submit()
                    frappe.db.commit()

# def create_od():
#     ods = frappe.db.sql("select `tabOn Duty Application`.name as name, `tabOn Duty Application`.from_date as from_date,`tabMulti Employee`.employee as employee from `tabOn Duty Application` left join `tabMulti Employee` on `tabOn Duty Application`.name = `tabMulti Employee`.parent where `tabMulti Employee`.employee = 'TSAI0266' ",as_dict=True)
#     # print(ods)
#     for od in ods:
#         att = frappe.db.exists("Attendance",{"attendance_date":od.from_date,"employee":od.employee,"docstatus":["!=","2"]})
#         if not att:
#             doc = frappe.new_doc("Attendance")
#             doc.employee = od.employee
#             doc.attendance_date = od.from_date
#             doc.status = 'Present'
#             doc.on_duty_application = od.name
#             doc.save(ignore_permissions=True)
#             doc.submit()
#             frappe.db.commit()


# def method():
#     frappe.db.set_value('Attendance Summary',None,'employee_name',None)

@frappe.whitelist()
def fetch_sap_stock():
    # parts = frappe.get_all('Part Master',['mat_no','name'])
    # for part in parts:
    url = "http://172.16.1.18/StockDetail/Service1.svc/GetFGQuantity"
    date = str(add_days(today(), -1)).replace('-', '')
    # date = "20220125"
    print(date)
    payload = json.dumps({
        "Fromdate": date,
        "Todate": date,
        "ItemCode": ""
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    sap_stock = json.loads(response.text)
    if sap_stock:
        d = pd.to_datetime(date)
        frappe.db.sql(
            "delete from `tabSAP Outgoing Report` where ar_invoice_date between '%s' and '%s' " % (date, date))
        for ss in sap_stock:
            ar_invoice_date = pd.to_datetime(ss['AR_Invoice_Date'])
            ar_invoice_date = ar_invoice_date.to_pydatetime()
            ar_invoice_date = ar_invoice_date.date()
            # sapog_id = frappe.db.exists("SAP Outgoing Report",{"ar_invoice_date":ar_invoice_date,"ar_invoice_no": ss['AR_Invoice_No']})
            # if sapog_id:
            #     sapog = frappe.get_doc("SAP Outgoing Report",sapog_id)
            # else:
            sapog = frappe.new_doc("SAP Outgoing Report")
            sapog.update({
                "ar_invoice_date": ar_invoice_date,
                "ar_invoice_no": ss['AR_Invoice_No'],
                "base_price": ss['Base_Price'],
                "base_value": ss['Base_Value'],
                "customer_code": ss['Customer_Code'],
                "customer_name": ss['Customer_Name'],
                "customer_ref_no": ss['Customer_Ref_No'],
                "item_service_description": ss['Dscription'],
                "fm": ss['FM'],
                "part_no": ss['PartNo'],
                "quantity": ss['Qty'],
                "sales_price": ss['Sales_Price'],
                "sales_value": ss['Sales_Value'],
            })
            sapog.save(ignore_permissions=True)
            frappe.db.commit()


@frappe.whitelist()
def test_hook():
    frappe.log_error(title='hooks', message='ok')


def create_hooks():
    job = frappe.db.exists('Scheduled Job Type', 'overall_invoice_key_download_evening')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")
        sjt.update({
            "method": 'thaisummit.thaisummit.doctype.ekanban_settings.ekanban_settings.enqueue_overall_invoice_key_cron',
            "frequency": 'Cron',
            "cron_format": '05 16 * * *'
        })
        sjt.save(ignore_permissions=True)

def create_hooks():
    job = frappe.db.exists('Scheduled Job Type', 'open_production_qty')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")
        sjt.update({
            "method": 'thaisummit.utils.get_open_production_qty',
            "frequency": 'Cron',
            "cron_format": '0,30 * * * *'
        })
        sjt.save(ignore_permissions=True)


@frappe.whitelist()
def fetch_sap_stock_bulk():
    # parts = frappe.get_all('Part Master',['mat_no','name'])
    # for part in parts:
    url = "http://172.16.1.18/StockDetail/Service1.svc/GetFGQuantity"
    date = str(add_days(today(), -1)).replace('-', '')
    print(date)
    payload = json.dumps({
        "Fromdate": "20211109",
        "Todate": "20211109",
        "ItemCode": ""
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    sap_stock = json.loads(response.text)
    if sap_stock:
        for ss in sap_stock:
            ar_invoice_date = pd.to_datetime(ss['AR_Invoice_Date'])
            ar_invoice_date = ar_invoice_date.to_pydatetime()
            ar_invoice_date = ar_invoice_date.date()
            # sapog_id = frappe.db.exists("SAP Outgoing Report",{"ar_invoice_date":ar_invoice_date,"ar_invoice_no": ss['AR_Invoice_No']})
            # if sapog_id:
            #     sapog = frappe.get_doc("SAP Outgoing Report",sapog_id)
            # else:
            sapog = frappe.new_doc("SAP Outgoing Report")
            sapog.update({
                "ar_invoice_date": ar_invoice_date,
                "ar_invoice_no": ss['AR_Invoice_No'],
                "base_price": ss['Base_Price'],
                "base_value": ss['Base_Value'],
                "customer_code": ss['Customer_Code'],
                "customer_name": ss['Customer_Name'],
                "customer_ref_no": ss['Customer_Ref_No'],
                "item_service_description": ss['Dscription'],
                "fm": ss['FM'],
                "part_no": ss['PartNo'],
                "quantity": ss['Qty'],
                "sales_price": ss['Sales_Price'],
                "sales_value": ss['Sales_Value'],
            })
            sapog.save(ignore_permissions=True)
            frappe.db.commit()


@frappe.whitelist()
def fetch_sap_production():
    url = "http://172.16.1.18/StockDetail/Service1.svc/GetProductionPlanQty"
    from_date = str(add_days(today(), -1)).replace('-', '')
    to_date = str(today()).replace('-', '')
    # from_date = '20220131'
    # to_date = '20220210'
    print(from_date)
    print(to_date)
    payload = json.dumps({
        "Fromdate": from_date,
        "Todate": to_date
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    sap_production = json.loads(response.text)
    print(sap_production)
    if sap_production:
        frappe.db.sql("delete from `tabSAP Production Plan` where order_date between '%s' and '%s' " % (
            pd.to_datetime(from_date).date(), pd.to_datetime(to_date).date()))
        for sp in sap_production:
            order_date = datetime.strptime(sp['OrderDate'], '%d-%m-%Y').date()
            due_date = datetime.strptime(sp['DueDate'], '%d-%m-%Y').date()
            start_date = datetime.strptime(sp['StartDate'], '%d-%m-%Y').date()
            # due_date = pd.to_datetime(sp['DueDate'])
            # due_date = due_date.to_pydatetime()
            # order_date = pd.to_datetime(sp['OrderDate'])
            # order_date = order_date.to_pydatetime()
            # start_date = pd.to_datetime(sp['StartDate'])
            # start_date = start_date.to_pydatetime()
            sappp = frappe.new_doc("SAP Production Plan")
            sappp.update({
                "completed_quantity": sp['CompletedQty'],
                "doc_no": sp['DocNum'],
                "doc_series": sp['DocSeries'],
                "due_date": due_date,
                "open_quantity": sp['OpenQty'],
                "order_date": order_date,
                "planned_quantity": sp['PlanQty'],
                "product_description": sp['ProdDesc'],
                "product_no": sp['ProdNo'],
                "rejected_quantity": sp['RejectedQty'],
                "select": sp['Select'],
                "start_date": start_date,
                "status": sp['Status'],
                "type": sp['Type']
            })
            sappp.save(ignore_permissions=True)
            frappe.db.commit()

# def add_payslip_role():
#     emps = frappe.get_all('Employee',{'employee_type':('in',('WC','BC','NT','FT'))},'user_id')
#     for emp in emps:
#         if emp.user_id:
#             user = frappe.get_doc('User',emp.user_id)
#             user.add_roles('Salary Slip')
#             user.save(ignore_permissions=True)
#             frappe.db.commit()


def add_role():
    user = frappe.get_doc('User', 'yukesh.sri@thaisummit.co.in')
    # user.remove_roles('HR Manager')
    # user.add_roles('Sales User')
    user.save(ignore_permissions=True)
    frappe.db.commit()


@frappe.whitelist()
def get_dispatch_data(doc):
    i = 1
    data = """
            <thead>
            <tr>
            <th>SL.No</th>
            <th>CARD RECIEVED DATE & TIME</th>
            <th>EXPECTED DISPATCH ON</th>
            <th>DISPATCH DATE & TIME</th>
            <th>MAT NO</th>
            <th>PART NO</th>
            <th>PART NAME</th>
            <th>MODEL</th>
            <th>DISPATCH QTY</th>
            <th>SAP STOCK</th>
            <th>DISPATCH READINESS STATUS</th>
            </tr>
            </thead>
    """
    for row in doc.tag_wise_list:
        exp_dispatch_time = datetime.strptime(
            str(row.datetime), "%Y-%m-%d %H:%M:%S") + timedelta(minutes=55)
        frappe.errprint(exp_dispatch_time)
        frappe.errprint(type(exp_dispatch_time))
        data += """
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td></td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td></td>
        </tr>""" % (i, row.datetime, exp_dispatch_time, row.mat_no, row.parts_no, row.parts_name, row.model, row.required_quantity, row.sap_quantity)
        i += 1

    return cstr(data)


# @frappe.whitelist()
# def remove_late(filename):
#     from frappe.utils.file_manager import get_file
#     filepath = get_file(filename)
#     pps = read_csv_content(filepath[1])
#     for pp in pps:
#         att = frappe.get_doc("Attendance",{'employee':pp[0],'attendance_date':pp[1]})
#         frappe.db.set_value('Attendance',att.name,'manually_corrected',1)
#         print(pp[1])
#         # frappe.db.set_value('Attendance',att.name,'status','Present')
#         # frappe.db.set_value('Attendance',att.name,'shift_status','')
#         # frappe.db.set_value('Attendance',att.name,'leave_type','')


# @frappe.whitelist()
# def update_department():
#     emps = frappe.get_all("Employee",{'status':'Active'},['user_id','department'])
#     for emp in emps:
#         print(emp)
#         if emp.user_id:
#             if not frappe.db.exists("User Permission",{'user':emp.user_id,'allow':"Department","for_value":emp.department,"is_default":1}):
#                 default = frappe.db.exists("User Permission",{'user':emp.user_id,'allow':"Department","is_default":'1'})
#                 if default:
#                     frappe.delete_doc("User Permission",default)
#                 up = frappe.db.exists("User Permission",{'user':emp.user_id,'allow':"Department",'for_value':emp.department})
#                 if up:
#                     doc = frappe.get_doc("User Permission",up)
#                     doc.is_default = 1
#                     doc.save(ignore_permissions=True)
#                 else:
#                     doc = frappe.new_doc("User Permission")
#                     doc.user = emp.user_id
#                     doc.allow = "Department"
#                     doc.for_value = emp.department
#                     doc.is_default = 1
#                     doc.save(ignore_permissions=True)

def run_method():
    # frappe.db.set_value('Overtime Request','OT-32935','total_hours','23:00')

    ots = frappe.db.sql('select name,employee from `tabOvertime Request` where department is null ',as_dict=True)
    for ot in ots:
        print(ot)
        dept = frappe.db.get_value('Employee',{'name':ot.employee},'department')
        print(dept)
        frappe.db.set_value('Overtime Request',ot.name,'department',dept)
    # frappe.db.set_value('Attendance','HR-ATT-2022-90346','out_time','2022-02-25 02:39')
    # emps = ["MOS0674",
    #         "NT0185",
    #         "MOS0771",
    #         "T0992",
    #         "JMS1591",
    #         "T1333",
    #         "NT0186",
    #         "VRV2212",
    #         "JMS1399",
    #         "JMS1345",
    #         "NT0158",
    #         ]
    # for emp in emps:
    #     ot = frappe.db.exists("Overtime Request",{'employee':emp,'ot_date':'2022-01-30'})
    #     print(ot)
    #     hr = frappe.db.get_value('Overtime Request',ot,'ot_hours')
    #     print(hr)
    #     frappe.db.set_value('Overtime Request',ot,'shift','1')
    #     frappe.db.set_value('Overtime Request',ot,'from_time','08:00')
    #     frappe.db.set_value('Overtime Request',ot,'to_time','01:00')
    #     frappe.db.set_value('Overtime Request',ot,'total_hours','23:00')
    #     frappe.db.set_value('Overtime Request',ot,'ot_hours','23:00')
    #     print('hi')

    # atts = frappe.db.sql("""select name,time,employee from `tabEmployee Checkin` where date(time) between '2022-02-08' and '2022-02-08' and attendance is null """,as_dict=True)
    # print(len(atts))
    # i = 0
    # for att in atts:
    #     count = frappe.db.count("Employee Checkin",{'employee':att.employee,'time':att.time})
    #     if count >= 2:
    #         print(i)
    #         frappe.delete_doc('Employee Checkin',att.name)
    #         i += 1

    # check = frappe.db.sql("select time from `tabEmployee Checkin` where date(time) = '2022-02-05' and employee = 'SRA1010' ",as_dict=True)
    # for c in check:
    #     print(c.time.nanosecond)
#     frappe.db.set_value('Overtime Request','OT-26654','workflow_state','Draft')
    # filepath = get_file(file)
    # pps = read_csv_content(filepath[1])
    # for pp in pps:
    #     if frappe.db.exists("Employee",pp[5]):
    #         print(pp[1])
    #         t = datetime.strptime(pp[1], '%d-%b-%Y %H:%M:%S')
    #         t = t.replace(second=0)
    #         if not frappe.db.exists("Employee Checkin",{'employee':pp[5],'time':t}):
    #             doc = frappe.new_doc("Employee Checkin")
    #             doc.employee = pp[5]
    #             doc.time = t
    #             doc.log_type = pp[2].upper()
    #             doc.save(ignore_permissions=True)
    #             frappe.db.commit()

    # atts = frappe.db.sql("""select name,time,employee from `tabEmployee Checkin` where date(time) between '2022-01-26' and '2022-02-04' and attendance is null """,as_dict=True)
    # print(len(atts))
    # i = 0
    # for att in atts:
    #     count = frappe.db.count("Employee Checkin",{'employee':att.employee,'time':att.time})
    #     if count >= 2:
    #         print(i)
    #         frappe.delete_doc('Employee Checkin',att.name)
    #         i += 1

    # sql = frappe.db.sql("""delete from `tabEmployee Checkin` where name in ()""")
    # atts = frappe.get_all('Attendance',{'employee':'TSAI0093','docstatus':'2'})
    # print(len(atts))
    # for att in atts:
    #     frappe.db.set_value('Attendance',att,'docstatus',0)
    # for emp in emps:
    #     ot = frappe.db.exists('Overtime Request',{'employee':emp,'ot_date':'2022-01-17'})
    # #     frappe.db.set_value('Overtime Request',ot,'shift','1')
    # #     frappe.db.set_value('Overtime Request',ot,'from_time','08:00:00')
    # #     frappe.db.set_value('Overtime Request',ot,'to_time','01:00:00')
    # #     frappe.db.set_value('Overtime Request',ot,'ot_hours','15:00:00')
    #     ts = frappe.db.exists('Timesheet',{'overtime_request':ot})
    # #     print(emp)
    # #     print('-----------')
    #     frappe.db.set_value('Timesheet',ts,'total_hours','16')
    # #     frappe.db.set_value('Timesheet',ts,'docstatus','1')

#     checks = frappe.db.sql("""select * from `tabEmployee Checkin` where date(time) = '2022-01-24' """,as_dict=True)
#     for c in checks:
#         print(c.time)
#         time = pd.to_datetime(c.time).replace(second=0)
#         print(time)
#         frappe.db.set_value('Employee Checkin',c.name,'time',time)
#     qrs = frappe.get_all("QR Checkin",{'shift_date':'2022-01-24','ot':'1','department':'WELD-IYM'},['*'])
#     for qr in qrs:
#         print(qr.name)
#         if not frappe.db.exists("Overtime Request",{'ot_date':qr.shift_date,'employee':qr.employee,'shift':qr.qr_shift}):
#             print('ot')
#             ot = frappe.new_doc('Overtime Request')
#             ot.employee = qr.employee
#             ot.department = qr.department
#             ot.ot_date = qr.shift_date
#             ot.shift = qr.qr_shift
#             shift_start = frappe.db.get_value('Shift Type',qr.qr_shift,"start_time")
#             shift_start_time = datetime.strptime(str(shift_start), '%H:%M:%S')
#             qr_shift = datetime.strptime(str(qr.created_date), '%Y-%m-%d')
#             ot.from_time = datetime.combine(qr_shift,shift_start_time.time())
#             ot.to_time = ""
#             ot.total_hours = ""
#             ot.total_wh = ""
#             ot.ot_hours = ""
#             ot.save(ignore_permissions=True)
#             frappe.db.commit()

    # frappe.db.set_value('IYM Sequence Plan Upload','IYMP0038','docstatus',0)
    # ss = frappe.get_all('Salary Slip',{'employee_type':'CL'},['name','employee'])
    # for s in ss:
    #     con = frappe.db.get_value('Employee',s.employee,'contractor')
    #     frappe.db.set_value('Salary Slip',s.name,'contractor',con)
    # atts = frappe.get_all('Attendance',{'attendance_date':('between',('2021-10-26','2021-11-25')),'employee_type':'CL','docstatus':0})
    # for att in atts:
    #     print(att.name)
    #     at = frappe.get_doc('Attendance',att.name)
    #     at.submit()
    # las = frappe.get_all('Leave Ledger Entry',{'from_date':'2021-12-26','leave_type':'Earned Leave','transaction_type':'Leave Allocation'},['transaction_name','name','employee','employee_name'])
    # for la in las:
    #     if not frappe.db.exists('Leave Allocation',la.transaction_name):
    #         frappe.db.sql("delete from `tabLeave Ledger Entry` where name = '%s' "%la.name)
    # frappe.db.set_value('Leave Allocation',la.name,'docstatus',1)
    # frappe.db.set_value('Leave Ledger Entry','28b207b38a','from_date','2021-12-25')
    # las = frappe.get_all('Leave Ledger Entry',{'from_date':'2021-12-31','is_expired':'1'})
    # for la in las:
    #     print(la)
    #     frappe.db.set_value('Leave Ledger Entry',la.name,'from_date','2021-12-25')
    #     frappe.db.set_value('Leave Allocation',la.name,'to_date','2021-12-25')
    #     frappe.db.set_value('Leave Ledger Entry',{'transaction_name':la.name},'to_date','2021-12-25')
    # doc = frappe.new_doc("QR Checkin")
    # doc.employee = 'NT0184'
    # doc.qr_shift = '1'
    # doc.qr_scan_time = '2021-11-24 08:30',
    # doc.created_date = '2021-11-24'
    # doc.shift_date = '2021-11-24'
    # doc.employee_name = frappe.db.get_value('Employee','NT0184','employee_name')
    # doc.employee_type = frappe.db.get_value('Employee','NT0184','employee_type')
    # doc.department = frappe.db.get_value('Employee','NT0184','department')
    # doc.save(ignore_permissions=True)
    # frappe.db.commit()
    # for emp in emps:
    #     print(emp)
    #     frappe.db.set_value('Employee',emp,'status','Left')
    #     frappe.db.set_value('Employee',emp,'relieving_date','2021-10-25')

#     las = frappe.get_all('Leave Ledger Entry',{'from_date':'2021-10-08','to_date':'2021-12-31','leave_type':'Special Leave'})
#     for la in las:
#         print(la.name)
#         frappe.db.set_value('Leave Ledger Entry',la.name,'to_date','2021-10-11')
    # frappe.db.set_value('Attendance','HR-ATT-2021-308972','leave_application','')
    # frappe.db.set_value('Attendance','HR-ATT-2021-308972','leave_type','')

# @frappe.whitelist()
# def update_department():
#     emps = frappe.get_all("Employee",{'name':'T1606'},['name','department'])
#     for emp in emps:
#         print(emp)
#         qrs = frappe.get_all('QR Checkin',{'employee':emp.name})
#         for qr in qrs:
#             frappe.set_value('QR Checkin',qr.name,'department','WELD-RE J LINE')

# def delete_att():
#     emps = frappe.get_all("Employee",{'status':'Left','employee_type':'CL','relieving_date':('>','2021-09-25')},['name','relieving_date'])
#     for emp in emps:
#         print(emp)
#         atts = frappe.get_all('Attendance',{'employee':emp.name,'attendance_date':('>',emp.relieving_date),'docstatus':('!=','2')})
#         for att in atts:
#             checkins = frappe.get_all('Employee Checkin',{'attendance':att.name})
#             for c in checkins:
#                 frappe.db.set_value('Employee Checkin',c.name,'attendance','')
#             qrs = frappe.get_all('QR Checkin',{'attendance':att.name})
#             for qr in qrs:
#                 frappe.db.set_value('QR Checkin',qr.name,'attendance','')

#             attendance = frappe.get_doc('Attendance',att.name)
#             try:
#                 attendance.cancel()
#                 frappe.delete_doc('Attendance',attendance.name)
#             except:
#                 frappe.delete_doc('Attendance',attendance.name)


def delete_left_att(doc, method):
    atts = frappe.get_all('Attendance', {'employee': doc.name, 'attendance_date': (
        '>', doc.relieving_date), 'docstatus': ('!=', '2')})
    for att in atts:
        checkins = frappe.get_all('Employee Checkin', {'attendance': att.name})
        for c in checkins:
            frappe.db.set_value('Employee Checkin', c.name, 'attendance', '')

        attendance = frappe.get_doc('Attendance', att.name)
        try:
            attendance.cancel()
            frappe.delete_doc('Attendance', attendance.name)
        except:
            frappe.delete_doc('Attendance', attendance.name)


# def att_api():
#     url = "http://182.156.241.11/api/resource/Employee Checkin"
#     payload = 'data = {"employee": "TSAI0195","time":"2021-12-01 01:01"}'
#     headers = {
#     'Content-Type': 'application/json'
#     }
#     response = requests.request('POST',url,headers=headers,data=payload,verify='/etc/ssl/certs/nginx.crt')
#     print(response.text)

# def api_method():
#     url = "http://182.156.241.11/api/method/thaisummit.custom.mark_checkin?dn=Employee Checkin"
#     payload = json.dumps({
#     "employee": "TSAI0195",'time':'2021-12-01 01:01'
#     })
#     headers = {
#     'Content-Type': 'application/json'
#     }
#     response = requests.request('GET',url,headers=headers,verify='/etc/ssl/certs/nginx.crt')
#     print(response.text)


@frappe.whitelist(allow_guest=True)
def mark_checkin(**args):
    time = datetime.strptime(args['time'], '%Y%m%d%H%M%S')
    frappe.log_error(title="checkin", message=args)
    if not frappe.db.exists('Employee Checkin', {'employee': args['employee'], 'time': time}):
        frappe.log_error(title="checkin error", message=args)
        if args['deviceid'] == '01':
            log_type = 'IN'
        if args['deviceid'] == '02':
            log_type = 'OUT'
        try:
            ec = frappe.new_doc('Employee Checkin')
            ec.employee = args['employee'].upper()
            ec.time = time
            ec.log_type = log_type
            ec.save(ignore_permissions=True)
            frappe.db.commit()
            return "Checkin Marked"
        except:
            frappe.log_error(title="checkin error", message=args)
    else:
        return "Checkin Marked"

@frappe.whitelist()
def leave_application(leave_day,emp,leave_type,name,reason,approve):
    leave  = frappe.db.exists('Leave Application',{'from_date':leave_day,'employee':emp,'leave_type':leave_type})
    if leave :
        return leave
    else:
        doc = frappe.new_doc('Leave Allocation')
        doc.employee = emp
        doc.leave_type = leave_type
        doc.from_date = leave_day
        doc.to_date = leave_day
        doc.session = 'Full Day'
        doc.description = reason
        doc.leave_approver = approve
        doc.save(ignore_permissions=True)
        frappe.db.commit()

@frappe.whitelist()
def coff_leave(att_date,emp_id):
    if frappe.db.exists('Attendance',{'attendance_date':att_date,'employee':emp_id}):
        att = frappe.get_doc('Attendance',{'attendance_date':att_date,'employee':emp_id})
        twh = att.out_time - att.in_time
        time = datetime.strptime(str(twh),'%H:%M:%S').strftime('%H:%M')
        return att.in_time,att.out_time,time,att.shift
    
# @frappe.whitelist()
# def fetch_bom_details():
#     # parts = frappe.get_all('Part Master',['mat_no','name'])
#     # for part in parts:
#     url = "http://172.16.1.18/StockDetail/Service1.svc/GetBOMDetails"
#     payload = json.dumps({
#     # "Fromdate": add_days(today(),-2),
#     "ItemCode":"",
#     # "Todate": add_days(today(),-2)
#     })
#     headers = {
#     'Content-Type': 'application/json'
#     }
#     response = requests.request("POST", url, headers=headers, data=payload)
#     bom_deatils = json.loads(response.text)
#     print(len(bom_deatils))

# def bulk_upload_BOM_csv(filename):
#     from frappe.utils.file_manager import get_file
#     _file = frappe.get_doc('File',{'file_name':filename})
#     filepath = get_file(filename)
#     pps = read_csv_content(filepath[1])
#     for pp in pps:
#         print(pp)
#         doc = frappe.new_doc('TSAI BOM')
#         doc.item = pp[0]
#         doc.item_description = pp[1]
#         doc.uom = pp[2]
#         doc.item_quantity = pp[3]
#         doc.whse = pp[4]
#         doc.price = pp[5]
#         doc.depth = pp[6]
#         doc.bom_type = pp[7]
#         doc.fm = pp[8]
#         doc.save(ignore_permissions=True)
#         frappe.db.commit()


def group_by():
    # data = [['10000001',50,'sdfs00'],
    # ['31000001', 500,'sdfasdf'],
    # ['10000001', 200,'sdfs00'],
    # ['31000002', 200,'j'],
    # ['31000002', 200,'2']]

    import pandas as pd
    # df = pd.DataFrame(data, columns = ['Name', 'Age','test'])
    # df2 = df.groupby(['Name','test'])['Age'].sum().reset_index()
    # l = df2.values.tolist()
    data = [['abcd', 'asdfs'], ['sasddfs', 'assdf']]
    cols = ['1', '2']

    df = pd.DataFrame(data, columns=cols)
    print(df)
    # print(df2)
    # print(l)

# def update_mp():
#     mps = frappe.db.sql("select employee,name,attendance_date from `tabMiss Punch Application` where attendance is null",as_dict=True)
#     i = 1
#     for mp in mps:
#         att = frappe.db.get_value('Attendance',{'employee':mp.employee,'attendance_date':mp.attendance_date,'docstatus':('!=','2')})
#         frappe.db.set_value('Miss Punch Application',mp.name,'attendance',att)
#         m = frappe.get_doc('Miss Punch Application',mp.name)
#         frappe.db.set_value("Attendance",att,"in_time",m.in_time)
#         frappe.db.set_value("Attendance",att,"out_time",m.out_time)
#         frappe.db.set_value("Attendance",att,"qr_shift",m.qr_shift)
#         frappe.db.set_value("Attendance",att,"status","Present")
#         if not frappe.db.get_value("Attendance",m.attendance,"shift"):
#             frappe.db.set_value("Attendance",mp.attendance,"shift",m.qr_shift)


def check_ot():
    ots = frappe.db.sql("""select `tabOvertime Request`.employee as employee,`tabOvertime Request`.ot_hours as ot_hours from `tabOvertime Request` left JOIN 
    `tabEmployee` on `tabOvertime Request`.employee = `tabEmployee`.name where `tabEmployee`.employee_type = 'TH' and `tabOvertime Request`.ot_date between '2021-10-26' and '2021-11-25' and `tabOvertime Request`.workflow_state in ('Pending for HOD','Approved') and `tabOvertime Request`.docstatus != '2' """, as_dict=1)
    for ot in ots:
        print(ot)

# def check_timesheet():
#     ots = frappe.get_all("Overtime Request",{'workflow_state':'Approved','ot_date':('between',('2021-11-26','2021-12-25'))},['*'])
#     for ot in ots:
#         t = frappe.db.count('Timesheet',{'employee':ot.employee,'start_date':ot.ot_date,'docstatus':'1'})
#         if t == 2:
#             print(ot.name)

# def bulk_late():
#     from frappe.utils.file_manager import get_file
#     filepath = get_file('Late Report.csv')
#     pps = read_csv_content(filepath[1])
#     for pp in pps:
#         # print(pd.to_datetime(pp[1]).date())
#         att = frappe.db.exists('Attendance',{'employee':pp[0],'attendance_date':pd.to_datetime(pp[1]).date()})
#         print(pp[0])
#         print(att)
#         frappe.db.set_value('Attendance',att,'status','Present')
#         frappe.db.set_value('Attendance',att,'shift_status',pp[2])
#         frappe.db.set_value('Attendance',att,'manually_corrected',1)
# @frappe.whitelist()
# def ot_request():
#    ot = frappe.db.get_all('Overtime Request',{'ot_date':'2022-04-15','shift':'2','ot_hours':'14:00','employee':'SBE0868'},['name','employee','ot_hours'])
#    for o in ot:
#         if o:
#             frappe.db.set_value('Overtime Request',o.name,'ot_hours','15:00:00')
#             print('yes')

# @frappe.whitelist()
# def timesheet():
#     ot = frappe.db.sql(""" delete from `tabOvertime Request` where ot_date = '2022-04-16' and ot_hours = '14:00' """)
#     print(ot)
#     # ot = frappe.db.get_all('Overtime Request',{'ot_date':'2022-04-15','shift':'2','ot_hours':'14:00','employee':'SBE0868'},['name','employee','ot_hours'])
#     # for o in ot:
#     #     time = frappe.db.get_all('Timesheet',{'overtime_request':o.name},['total_hours'])
#     #     for t in time:
#     #         print(t)


@frappe.whitelist()
def ot():
    ot_request = frappe.db.sql(""" delete from `tabOvertime Request` where ot_date = '2022-04-24' and ot_hours = '14:00' """)
    print(ot_request)

# @frappe.whitelist()
# def shift(current_time):
#     if ('06:30') < current_time < ('10:00'):
#         return '1 Shift'

@frappe.whitelist()
def checkins():
#     first_aid = frappe.db.sql(""" select `tabMedicine Table`* from `tabFirst Aid` where date = '2022-06-13' """)
#     print(first_aid)leave
    # salary_slip = frappe.db.sql(""" select count (*)  from `tabSalary Slip` where start_date  between '2022-04-26' and '2022-05-25'  and employee_type = 'BC'  """)
    # print(salary_slip)
    # checkin = frappe.db.sql(""" select count(*) from `tabEmployee Checkin`  where date(time) = '2022-05-21' and employee_type like 'FT' """)
    # print(checkin)
    # checkin = frappe.db.sql(""" update `tabEmployee Checkin` set skip_auto_attendance = 0 where date(time) = '2022-05-21' and employee_type like 'FT' """)
    # print(checkin)
    # checkin = frappe.db.sql(""" select count(*) from   `tabQR Checkin` where created_date = '2022-05-21' and employee_type like 'FT' """)
    # print(checkin)
    # checkin = frappe.db.sql(""" update `tabQR Checkin` set attendance = '' where created_date = '2022-05-21' and employee_type like 'FT' """)
    # print(checkin)
    # checkin = frappe.db.sql(""" select count(*) from `tabAttendance` where attendance_date between '2022-06-09' and '2022-06-25' and employee = 'TSAI0259' """)
    # print(checkin)
    checkin = frappe.db.sql(""" delete from `tabAttendance` where attendance_date between  '2022-05-10' and '2022-06-28' and employee = 'TSAI0310' """)
    print(checkin)
    # shift = frappe.db.sql(""" delete from `tabShift Assignment` where start_date between '2022-06-06' and '2022-06-11' and department = 'Press-RE SPM' """)
    # print(shift)

@frappe.whitelist()
def get_dates():
    data = 0
    rate = [1,2,3,4,5]
    for i in rate:
        if i:
            data+= i
            print(data)

# @frappe.whitelist()
# def shift_check():
#     emp = frappe.db.get_value('Employee Checkin',{'employee':'NT0431','log_type':'OUT'},['time'])
#     # print(emp)
#     attendance = frappe.db.exists('Attendance',{'attendance_date':'2022-06-11','employee':'NT0431'})
#     att = frappe.db.set_value('Attendance',attendance,'out_time',emp)
#     print(attendance)
#     # print(att)

# @frappe.whitelist()
# def nt_att():
#     att = frappe.db.sql(""" delete from `tabSalary Slip` where start_date between '2022-05-26'  and '2022-06-25' and employee_type = 'BC' """)
#     print(att)
#     # error_log = frappe.db.sql(""" delete from `tabError Log`""")
#     # print(error_log)
 