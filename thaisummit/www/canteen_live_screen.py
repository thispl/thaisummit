from datetime import datetime
import frappe
from datetime import date


def get_context(context):
    if frappe.session.user != 'Guest':
        context.data = get_food_count()


@frappe.whitelist()
def get_food_count():
    data = {}
    current_date = date.today()
    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")
    frappe.errprint(current_datetime)
    food_count = 0
    food_type = get_food_time()
    if food_type == 'Break Fast':
        food_count = frappe.db.get_value('Food Plan',{'date':current_date},'bf_head_count')
        food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':food_type})
    elif food_type == 'Lunch':
        food_count =  frappe.db.get_value('Food Plan',{'date':current_date},['lbv_head_count']) 
        # if food_count [0] > 0:
        #     normal_lunch = food_count[0]
        # elif food_count[1] > 0:
        #     b_veg = food_count[1]  
        # elif food_count[2] > 0:
        #     b_non_veg = food_count[2]
        # elif food_count[3] > 0 :
        #     s_veg = food_count[3] 
        # elif food_count[4] > 0 :
        #     s_non_veg = food_count[4]
        # else:
        #     food_count[0]              
        food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':food_type})
        # if food_scan[0] > 0 :
        #     normal_lunch_count = food_scan[0]
        # elif food_scan [1] > 0:
        #     b_veg_count = food_scan[1]
        # elif food_scan[2] > 0 :
        #     b_non_veg_count = food_scan[2]
        # elif food_scan[3] > 0:
        #     s_veg_count = food_scan[3]
        # elif food_scan[4] > 0:
        #     s_non_veg_count = food_scan[4]
        # else:
        #     food_scan[0]                    
    elif food_type == 'Dinner':
        food_count = frappe.db.get_value('Food Plan',{'date':current_date},['dbv_head_count',])
        food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':food_type})
    elif food_type == 'Supper':
        food_count = frappe.db.get_value('Food Plan',{'date':current_date},'ssf_head_count')
        food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':food_type})
    else:
        food_type = 'NA' 
    data.update({
        "current_datetime":current_datetime,
        "food_type": food_type,
        "food_count":food_count,
        "food_scan":food_scan,
    })
    return data

@frappe.whitelist()
def get_live_screen_data():
    data = {}
    current_date = date.today()
    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")
    food_count = food_scan = 0
    lu_head_count  = lbv_head_count  = lbnv_head_count = lsv_head_count = lsnv_head_count = total_lunch_plan = 0
    total_lunch_actual = lu_food_scan = lbv_food_scan = lbnv_food_scan = lsv_food_scan = lsnv_food_scan = 0
    total_lunch_gap = lu_gap = lbv_gap = lbnv_gap = lsv_gap = lsnv_gap = 0
    food_type = get_food_time()
    if food_type == 'Break Fast':
        food_count = frappe.db.get_value('Food Plan',{'date':current_date},'bf_head_count')
        food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':food_type})
    elif food_type == 'Lunch':
        lu_head_count =  frappe.db.get_value('Food Plan',{'date':current_date},['lu_head_count'])
        lbv_head_count =  frappe.db.get_value('Food Plan',{'date':current_date},['lbv_head_count'])
        lbnv_head_count =  frappe.db.get_value('Food Plan',{'date':current_date},['lbnv_head_count'])
        lsv_head_count =  frappe.db.get_value('Food Plan',{'date':current_date},['lsv_head_count'])
        lsnv_head_count =  frappe.db.get_value('Food Plan',{'date':current_date},['lsnv_head_count'])
        total_lunch_plan = lu_head_count + lbv_head_count + lbnv_head_count + lsv_head_count + lsnv_head_count
        lu_food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':"Lunch"})
        lbv_food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':"Lunch Briyani Veg"})
        lbnv_food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':"Lunch Briyani Non Veg"})
        lsv_food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':"Lunch Special Veg"})
        lsnv_food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':"Lunch Special Non Veg"})
        total_lunch_actual = lu_food_scan + lbv_food_scan + lbnv_food_scan + lsv_food_scan + lsnv_food_scan
        lu_gap = lu_head_count -  lu_food_scan
        lbv_gap = lbv_head_count -  lbv_food_scan
        lbnv_gap = lbnv_head_count -  lbnv_food_scan  
        lsv_gap = lsv_head_count -  lsv_food_scan
        lsnv_gap = lsnv_head_count -  lsnv_food_scan
        total_lunch_gap = lu_gap + lbv_gap + lbnv_gap + lsv_gap + lsnv_gap
    elif food_type == 'Dinner':
        food_count = frappe.db.get_value('Food Plan',{'date':current_date},['dbv_head_count',])
        food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':food_type})
    elif food_type == 'Supper':
        food_count = frappe.db.get_value('Food Plan',{'date':current_date},'ssf_head_count')
        food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':food_type})
    else:
        food_type = 'NA' 
    data.update({
        "current_datetime":current_datetime,
        "food_type": food_type,
        "lu_head_count":lu_head_count,
        "lbv_head_count":lbv_head_count,
        "lbnv_head_count":lbnv_head_count,
        "lsv_head_count":lsv_head_count,
        "lsnv_head_count":lsnv_head_count,
        "total_lunch_plan":total_lunch_plan,
        "lu_food_scan":lu_food_scan,
        "lbv_food_scan":lbv_food_scan,
        "lbnv_food_scan":lbnv_food_scan,
        "lsv_food_scan":lsv_food_scan,
        "lsnv_food_scan":lsnv_food_scan,
        "total_lunch_actual":total_lunch_actual,
        "lu_gap":lu_gap,
        "lbv_gap":lbv_gap,
        "lbnv_gap":lbnv_gap,
        "lsv_gap":lsv_gap,
        "lsnv_gap":lsnv_gap,
        "total_lunch_gap":total_lunch_gap,
        "food_count":food_count,
        "food_scan":food_scan,
    })
    return data


def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]


def get_food_time():
    from datetime import datetime
    from datetime import date, timedelta,time
    nowtime = datetime.now()
    shift_date = date.today()
    shift1_time = [time(hour=6, minute=0, second=0),time(hour=7, minute=00, second=0)]
    shift2_time = [time(hour=8, minute=00, second=0),time(hour=16, minute=30, second=0)]
    shift3_time = [time(hour=17, minute=00, second=0),time(hour=23, minute=0, second=0)]
    shiftpp2_time = [time(hour=00, minute=0, second=1),time(hour=4, minute=0, second=0)]
    curtime = time(hour=nowtime.hour, minute=nowtime.minute, second=nowtime.second)
    food_type = 'NA'
    if is_between(curtime,shift1_time):
        food_type = 'Break Fast'
    if is_between(curtime,shift2_time):
        food_type = 'Lunch'
    if is_between(curtime,shift3_time):
        food_type = 'Dinner'
    if is_between(curtime,shiftpp2_time):
        food_type = 'Supper'
    return food_type 
