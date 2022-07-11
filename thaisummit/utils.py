import json
from re import M

import requests
import frappe
from frappe.utils import today, add_days, date_diff,cint

@frappe.whitelist()
def get_server_date():
    return today()

@frappe.whitelist()
def reset_supplier_invoice_no():
    suppliers = frappe.get_all('TSAI Supplier')
    for supplier in suppliers:
        frappe.db.set_value('TSAI Supplier',supplier,'current_running_no',0)

@frappe.whitelist()
def leave_restriction(leave,from_date):
    before = frappe.get_value('Leave Type',{'name':leave},['before'])*-1
    after = frappe.get_value('Leave Type',{'name':leave},['after'])
    if from_date > add_days(today(),after):
        return 'No'
    elif from_date < add_days(today(),before):
        return 'No'

@frappe.whitelist()
def leave_limit(employee,from_date,to_date,dept):
    if frappe.db.get_value('Employee',{'name':employee},['employee_type']) != 'WC':
        no_of_days = date_diff(add_days(to_date, 1),from_date )
        dates = [add_days(from_date, i) for i in range(0, no_of_days)]
        err = ''
        for date in dates:
            count = frappe.db.sql("""select count(name) as count from `tabLeave Application` where '%s' between from_date and to_date and department = '%s' and employee_type != 'WC' and docstatus != 2 """%(date,dept),as_dict=True)[0].count or 0
            # count = frappe.db.count("Leave Application",{"deptartment":dept,"from_date":date})
            dept_limit = frappe.get_value("Department",{'name':dept},['leave_limit'])
            if dept_limit != 0:
                if count >= dept_limit:
                    err += "Department wise Leave Limit exceeds for %s <br>"%(date)
        return err

def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]


@frappe.whitelist()
def get_open_production_qty():
    from datetime import date
    today = date.today()
    mat_nos = frappe.db.sql("""select mat_no from `tabTSAI Part Master`""",as_dict=1)
    # from_date = today.strftime("%Y%m%d")
    # to_date = add_days(today, -90)
    # today.strftime("%Y%m%d")
    for mat_no in mat_nos:
        url = "http://172.16.1.18/StockDetail/Service1.svc/GetOpenProductionOrder"
        payload = json.dumps({
            "ProductNo": mat_no['mat_no'],
            "Fromdate": "",
            "Todate": ""
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request(
            "POST", url, headers=headers, data=payload)
        openqty = 0
        if response:
            total_qty = 0
            stocks = json.loads(response.text)
            if stocks:
                openqty = stocks[0]['OpenQty']
                completed_qty = stocks[0]['CmpltQty']
                planned_qty = stocks[0]['PlannedQty']
                for stock in stocks:
                    total_qty += cint(stock['OpenQty'])
                opo = frappe.db.exists('Open Production Order',{'mat_no':mat_no})
                if opo:
                    opo_id = frappe.get_doc('Open Production Order')
                else:
                    opo_id = frappe.new_doc('Open Production Order')
                opo_id.update({
                    "daily_order_date": today,
                    "mat_no": mat_no['mat_no'],
                    "open_qty": total_qty,
                    "completed_qty": completed_qty,
                    "planned_qty": planned_qty
                })
                opo_id.save(ignore_permissions=True)
                frappe.db.commit()
                

@frappe.whitelist()
def get_bus_arrival_shift():
    from datetime import datetime
    from datetime import date, timedelta,time
    nowtime = datetime.now()
    std_shift_1_in_time = time(hour=7,minute=30,second=0)
    std_shift_2_in_time = time(hour=16,minute=15,second=0)
    std_shift_pp2_in_time = time(hour=19,minute=30,second=0)
    std_shift_3_in_time = time(hour=1,minute=0,second=0)
    shift1_time = [time(hour=6, minute=0, second=0),time(hour=15, minute=0, second=0)]
    shift2_time = [time(hour=15, minute=15, second=0),time(hour=18, minute=59, second=0)]
    shift3_time = [time(hour=23, minute=00, second=0),time(hour=2, minute=0, second=0)]
    shiftpp2_time = [time(hour=19, minute=0, second=1),time(hour=21, minute=59, second=0)]
    curtime = time(hour=nowtime.hour, minute=nowtime.minute, second=nowtime.second)
    shift_type = 'NA'
    status = 'Ontime'
    late_minutes = 0
    if is_between(curtime,shift1_time):
        shift_type = '1'
        if curtime > std_shift_1_in_time:
            status = 'Late'
            late_minutes = datetime.strptime(str(curtime),'%H:%M:%S') - datetime.strptime(str(std_shift_1_in_time),'%H:%M:%S')
    if is_between(curtime,shift2_time):
        shift_type = '2'
        if curtime > std_shift_2_in_time:
            status = 'Late'
            late_minutes = datetime.strptime(str(curtime),'%H:%M:%S') - datetime.strptime(str(std_shift_2_in_time),'%H:%M:%S')
    # if is_between(curtime,shift2_cont_time):
    #     shift_type = '2'
    if is_between(curtime,shift3_time):
        shift_type = '3'
        if curtime > std_shift_3_in_time:
            status = 'Late'
            late_minutes = datetime.strptime(str(curtime),'%H:%M:%S') - datetime.strptime(str(std_shift_3_in_time),'%H:%M:%S')

    if is_between(curtime,shiftpp2_time):
        shift_type = 'PP2'
        if curtime > std_shift_pp2_in_time:
            status = 'Late'
            late_minutes = datetime.strptime(str(curtime),'%H:%M:%S') - datetime.strptime(str(std_shift_pp2_in_time),'%H:%M:%S')

    return shift_type,status,late_minutes