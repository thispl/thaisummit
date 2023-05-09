import json
from operator import le
from re import M
import requests
import frappe
from frappe.utils import today, add_days, date_diff,cint,flt,get_time
from time import strptime
from datetime import datetime
import pandas as pd

@frappe.whitelist()
def ping():
    return frappe.get_value('TSAI Part Master',{'mat_no':'10000503'},'mat_type')

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
def get_live_stock():
    from datetime import date
    today = date.today()
    mat_nos = frappe.db.sql("""select mat_no from `tabTSAI Part Master` where mat_no like '10%'""",as_dict=1)
    # from_date = today.strftime("%Y%m%d")
    # to_date = add_days(today, -90)
    # today.strftime("%Y%m%d")
    for mat_no in mat_nos:
        url = "http://apioso.thaisummit.co.th:10401/api/GetItemInventory"
        payload = json.dumps({
            "ItemCode": mat_no['mat_no'],
        })
        headers = {
            'Content-Type': 'application/json',
            'API_KEY': '/1^i[#fhSSDnC8mHNTbg;h^uR7uZe#ninearin!g9D:pos+&terpTpdaJ$|7/QYups;==~w~!AWwb&DU',
        }
        response = requests.request(
            "POST", url, headers=headers, data=payload)
        stock = 0
        if response:
            stocks = json.loads(response.text)
            if stocks:
                ica = frappe.db.sql(
                    "select warehouse from `tabInventory Control Area` where invoice_key = 'Y' ", as_dict=True)

                wh_list = [d['warehouse'] for d in ica if 'warehouse' in d]

                df = pd.DataFrame(stocks)
                df = df[df['Warehouse'].isin(wh_list)]
                stock = pd.to_numeric(df["Qty"]).sum()
                lsq = frappe.db.exists('Live Stock Quantity',{'mat_no':mat_no['mat_no'],'live_stock_date':today})
                if lsq:
                    lsq_id = frappe.get_doc('Live Stock Quantity',lsq)
                else:
                    lsq_id = frappe.new_doc('Live Stock Quantity')
                lsq_id.update({
                    "live_stock_date": today,
                    "mat_no": mat_no['mat_no'],
                    "stock": stock
                })
                lsq_id.save(ignore_permissions=True)
                frappe.db.commit()

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
                opo = frappe.db.exists('Open Production Order',{'mat_no':mat_no['mat_no'],'daily_order_date':today})
                if opo:
                    opo_id = frappe.get_doc('Open Production Order',opo)
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
def get_open_production_qty_fg():
    from datetime import date
    today = date.today()
    url = "http://172.16.1.18/StockDetail/Service1.svc/GetOpenProductionOrder"
    payload = json.dumps({
        "ProductNo": "",
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
            for stock in stocks:
                openqty = flt(stock['OpenQty'])
                completed_qty = flt(stock['CmpltQty'])
                planned_qty = flt(stock['PlannedQty'])
                if openqty > 0:
                    mat_no = stock['ItemCode']
                    if frappe.db.exists('TSAI Part Master',mat_no):
                        opq = frappe.db.exists('Open Production Quantity',{'mat_no':mat_no,'daily_order_date':today})
                        if opq:
                            opq_id = frappe.get_doc('Open Production Quantity',opq)
                        else:
                            opq_id = frappe.new_doc('Open Production Quantity')
                        opq_id.update({
                            "daily_order_date": today,
                            "mat_no": mat_no,
                            "open_qty": openqty,
                            "completed_qty": completed_qty,
                            "planned_qty": planned_qty
                        })
                        opq_id.save(ignore_permissions=True)
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

@frappe.whitelist()
def get_previous_entry(emp,name):
    data  = ''
    # medicine_child = json.loads(medicine)
    previous_entry = frappe.db.exists('First Aid',{'id_no':emp})
    first_aid_previous = frappe.db.get_value('First Aid',{'name':previous_entry},['symptoms','prescription'])
    frappe.errprint(first_aid_previous)
    previous_first_aid_medicine = frappe.get_doc('Medicine Table',{'parent':previous_entry})
    frappe.errprint(previous_first_aid_medicine)
    data = "<table class='table table-bordered=1>"
    data += "<tr style='font-size:5px;padding:1px'><td style ='background-color:#ffedcc;border:1px solid black'>Emp ID</td><td style ='background-color:#ffedcc;border:1px solid black'>Employee Name</td><td style ='background-color:#ffedcc;border:1px solid black'>Symptoms</td><td style ='background-color:#ffedcc;border:1px solid black'>Prescription</td></tr>"
    data += "<tr style='font-size:5px;padding:1px'><td style ='background-color:#ffedcc;border:1px solid black'>History</td><td style ='background-color:#ffedcc;border:1px solid black'>Medicine Details</td></tr>"
    data += "<tr style='font-size:5px;padding:1px'><td style ='background-color:#ffedcc;border:1px solid black'>Emp ID</td><td style ='background-color:#ffedcc;border:1px solid black'>Previous Entry</td><td style ='background-color:#ffedcc;border:1px solid black'>Symptoms</td><td style ='background-color:#ffedcc;border:1px solid black'>Prescription</td><td style ='background-color:#ffedcc;border:1px solid black'>Medicine</td><td style ='background-color:#ffedcc;border:1px solid black'>Quantity</td><td style ='background-color:#ffedcc;border:1px solid black'>UOM</td></tr>"
    data += "<table>"

    return data


@frappe.whitelist()
def coff_leave(att_date,emp_id):
    data = []
    att = frappe.db.exists('Attendance',{'attendance_date':att_date,'employee':emp_id})
    if att:
        on_duty_check  = frappe.db.get_value('Attendance',{'name':att},['on_duty_application'])
        if on_duty_check:
           frappe.errprint('od')
        else:    
            attendance = frappe.db.get_value('Attendance',{'name':att},['in_time','out_time','shift'])
            twh = attendance[1] - attendance[0]
            twh_time = datetime.strptime(str(twh),'%H:%M:%S').strftime('%H:%M')
            frappe.errprint(twh_time)
            data.append(attendance[0])
            data.append(attendance[1])
            data.append(attendance[2])
            data.append(twh_time)
    return data

@frappe.whitelist()
def check_coff(emp_id,att_date):
    data = []
    att = frappe.db.exists('Attendance',{'attendance_date':att_date,'employee':emp_id})
    if att:
        on_duty_check  = frappe.db.get_value('Attendance',{'name':att},['on_duty_application'])
        if on_duty_check:
           data.append(on_duty_check)
    return data       

# @frappe.whitelist()
# def create_leave(doc,method):
#     leave_application = frappe.new_doc('Leave Application')
#     leave_application.employee = doc.employee
#     leave_application.leave_type = doc.leave_type
#     leave_application.from_date = doc.leave_on
#     leave_application.to_date = doc.leave_on
#     leave_application.session = "Full Day"
#     leave_application.reason = doc.reason
#     leave_application.save(ignore_permissions=True)
#     frappe.db.commit()

    # leave_application = frappe.new_doc('Leave Application')
    # leave_application.employee = emp
    # leave_application.leave_type = leave_type
    # leave_application.from_date = leave_date
    # leave_application.to_date = leave_date
    # leave_application.session = 'Full Day'
    # leave_application.reason = reason
    # leave_application.save(ignore_permissions=True)
    # frappe.db.commit()
    # return leave_application
    # if half_day:
    #     leave_application = frappe.new_doc('Leave Application')
    #     leave_application.employee = emp
    #     leave_application.leave_type = leave_type
    #     leave_application.from_date = leave_date
    #     leave_application.to_date = leave_date
    #     leave_application.half_day = 1
    #     leave_application.session = 'First Half'
    #     leave_application.reason = reason
    #     leave_application.save(ignore_permissions=True)
    #     frappe.db.commit()
    # else:
    #     leave_application = frappe.new_doc('Leave Application')
    #     leave_application.employee = emp
    #     leave_application.leave_type = leave_type
    #     leave_application.from_date = leave_date
    #     leave_application.to_date = leave_date
    #     leave_application.session = 'Full Day'
    #     leave_application.reason = reason
    #     leave_application.save(ignore_permissions=True)
    #     frappe.db.commit()

def test_api():
    total_tbs = frappe.db.sql("""select * from `tabTSAI Part Master` where mat_type in ('INH','BOP') and customer in ('IYM','HPS') """,as_dict=1)
    print(len(total_tbs))
    # fms = frappe.db.get_all('TSAI BOM',{'item':"21100001",'depth':('!=','1')},['fm','item_quantity'])
    # print(fms)
    
def create_hooks():
    job = frappe.db.exists('Scheduled Job Type', 'generate_re_production_plan')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")  
        sjt.update({
            "method" : 'thaisummit.api.generate_re_production_plan',
            # "frequency" : 'Daily'
            "frequency" : 'Cron',
            "cron_format" : '30 07 * * mon-sat'
        })
        sjt.save(ignore_permissions=True)



def check_dates():
    from_date = today()
    to_date = add_days(from_date,6)
    holiday = check_holiday(from_date,to_date)
    print(holiday)
    to_date = add_days(from_date,6 + len(holiday))
    d1 = datetime.strptime(from_date, "%Y-%m-%d")
    d2 = datetime.strptime(to_date, "%Y-%m-%d")
    print(from_date)
    print((d2 - d1).days)

def check_holiday(from_date,to_date):
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = 'Holiday List - 2021' and holiday_date between '%s' and '%s' """%(from_date,to_date),as_dict=True)
    return holiday

def get_dates(from_date,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates


@frappe.whitelist()
def ot_days():
    hr = frappe.db.get_single_value('HR Time Settings','overtime_validation_dates')
    print(hr)


def ot_amount_update():
    overtime = frappe.db.sql(""" select * from `tabOvertime Request` where ot_date between  '2023-02-26' and '2023-03-25' and workflow_state != 'Draft' and shift = 'PP2' and name = 'OT-98216' and ot_hours = '03:30' """,as_dict=True)
    for ot in overtime:
        if ot.ot_hours:
            if ot.employee_type != 'CL':
                basic = ((frappe.db.get_value('Employee',ot.employee,'basic')/26)/8)*2
                frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
                ftr = [3600,60,1]
                hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
                ot_hr = round(hr/3600,1)
                frappe.db.set_value('Overtime Request',ot.name,'ot_amount',round(ot_hr*basic))
            else:
                basic = 0
                designation = frappe.db.get_value('Employee',ot.employee,'designation')
                if designation == 'Skilled':
                    basic = frappe.db.get_single_value('HR Time Settings','skilled_amount_per_hour')
                elif designation == 'Un Skilled':
                    basic = frappe.db.get_single_value('HR Time Settings','unskilled_amount_per_hour')
                frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
                ftr = [3600,60,1]
                hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
                ot_hr = round(hr/3600,1)
                frappe.db.set_value('Overtime Request',ot.name,'ot_amount',round(ot_hr*basic))

# def ot_time_update():
#     ot_update = frappe.db.sql(""" update `tabOvertime Request` set total_hours = '03:30' where ot_date = '2023-03-18' and shift = 'PP2' and workflow_state != 'Draft' """)
#     ot_update_hours = frappe.db.sql(""" update `tabOvertime Request` set ot_hours = '03:30' where ot_date = '2023-03-18' and shift = 'PP2' and workflow_state != 'Draft' """)
#     print(ot_update)

@frappe.whitelist(allow_guest=True)
def sync_grn_data1(**args):
    return args