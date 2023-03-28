from datetime import datetime
import frappe
from datetime import date
from frappe.utils import flt
from frappe.utils.data import add_days, today
import json



# @frappe.whitelist()
# def canteen_time_settings(canteen):
#     canteens = json.loads(canteen)
#     for canteen in canteens:
#         if canteen['meal_type'] == 'Break Fast':
#             breakfast_min_time = datetime.strptime(str(canteen['min_time']),'%H:%M:%S').time()
#             frappe.errprint(breakfast_min_time.hour)
#             frappe.errprint(breakfast_min_time.minu)
#             frappe.errprint(breakfast_min_time.hour)

# def get_context(context):
#     if frappe.session.user != 'Guest':
#         context.data = get_food_count()

# @frappe.whitelist()
# def get_food_count():
#     data = {}
#     current_date = date.today()
#     current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")
#     frappe.errprint(current_datetime)
#     food_count = 0
#     food_type = get_food_time()
#     if food_type == 'Break Fast':
#         food_count = frappe.db.get_value('Food Plan',{'date':current_date},'bf_head_count')
#         food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':food_type})
#     elif food_type == 'Lunch':
#         food_count =  frappe.db.get_value('Food Plan',{'date':current_date},['lbv_head_count']) 
#         # if food_count [0] > 0:
#         #     normal_lunch = food_count[0]
#         # elif food_count[1] > 0:
#         #     b_veg = food_count[1]  
#         # elif food_count[2] > 0:
#         #     b_non_veg = food_count[2]
#         # elif food_count[3] > 0 :
#         #     s_veg = food_count[3] 
#         # elif food_count[4] > 0 :
#         #     s_non_veg = food_count[4]
#         # else:
#         #     food_count[0]              
#         food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':food_type})
#         # if food_scan[0] > 0 :
#         #     normal_lunch_count = food_scan[0]
#         # elif food_scan [1] > 0:
#         #     b_veg_count = food_scan[1]
#         # elif food_scan[2] > 0 :
#         #     b_non_veg_count = food_scan[2]
#         # elif food_scan[3] > 0:
#         #     s_veg_count = food_scan[3]
#         # elif food_scan[4] > 0:
#         #     s_non_veg_count = food_scan[4]
#         # else:
#         #     food_scan[0]                    
#     elif food_type == 'Dinner':
#         food_count = frappe.db.get_value('Food Plan',{'date':current_date},['dbv_head_count',])
#         food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':food_type})
#     elif food_type == 'Supper':
#         food_count = frappe.db.get_value('Food Plan',{'date':current_date},'ssf_head_count')
#         food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':food_type})
#     else:
#         food_type = 'NA' 
#     data.update({
#         "current_datetime":current_datetime,
#         "food_type": food_type,
#         "food_count":food_count,
#         "food_scan":food_scan,
#     })
#     return data



@frappe.whitelist()
def get_live_screen_data():
    data = {}
    current_date = date.today()
    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")

    bf_head_count = total_breakfast_plan =  0
    bf_food_scan = 0
    total_breakfast_actual = bf_food_scan = bf_actual_percent = 0
    total_bf_gap = bf_gap = bf_gap_percent = 0

    lu_head_count  = lbv_head_count  = lbnv_head_count = lsv_head_count = lsnv_head_count = total_lunch_plan = 0
    total_lunch_actual = lu_food_scan = lbv_food_scan = lbnv_food_scan = lsv_food_scan = lsnv_food_scan = lu_actual_percent = 0
    total_lunch_gap = lu_gap = lbv_gap = lbnv_gap = lsv_gap = lsnv_gap = lu_gap_percent = 0

    dn_head_count = dbv_head_count = dbnv_head_count = dsv_head_count = dsnv_head_count = total_dinner_plan = 0
    total_dinner_actual = dn_food_scan = dbv_food_scan = dbnv_food_scan = dsv_food_scan = dsnv_food_scan = dn_actual_percent =0
    total_dinner_gap = dn_gap = dbv_gap = dbnv_gap = dsv_gap = dsnv_gap = dn_gap_percent = 0

    sp_head_count = sd_head_count = ssf_head_count  = total_supper_plan = 0
    total_supper_actual = sp_food_scan = sd_food_scan = ssf_food_scan = sp_actual_percent = 0
    total_supper_gap = sp_gap = sd_gap = ssf_gap = sp_gap_percent =  0

    food_type = get_food_time()
    if food_type == 'Break Fast':
        bf_head_count = frappe.db.get_value('Food Plan',{'date':current_date},'bf_head_count')
        total_breakfast_plan = bf_head_count
        bf_food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':"Break Fast"})
        total_breakfast_actual = bf_food_scan
        bf_gap = bf_head_count - bf_food_scan
        total_bf_gap = bf_gap
        if total_breakfast_plan:
            bf_actual_percent = round(flt((total_breakfast_actual / total_breakfast_plan) * 100),2)
            bf_gap_percent = round(flt((total_bf_gap / total_breakfast_plan) * 100),2)

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
        if total_lunch_plan:
            lu_actual_percent = round(flt((total_lunch_actual / total_lunch_plan) * 100),2)
            lu_gap_percent = round(flt((total_lunch_gap / total_lunch_plan) * 100),2)


    elif food_type == 'Dinner':
        dn_head_count = frappe.db.get_value('Food Plan',{'date':current_date},['dn_head_count',])
        dbv_head_count = frappe.db.get_value('Food Plan',{'date':current_date},['dbv_head_count',])
        dbnv_head_count = frappe.db.get_value('Food Plan',{'date':current_date},['dbnv_head_count',])
        dsv_head_count = frappe.db.get_value('Food Plan',{'date':current_date},['dsv_head_count',])
        dsnv_head_count = frappe.db.get_value('Food Plan',{'date':current_date},['dsnv_head_count',])
        total_dinner_plan = dn_head_count + dbv_head_count + dbnv_head_count + dsv_head_count + dsnv_head_count
        dn_food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':"Dinner"})
        dbv_food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':"Dinner Briyani Veg"})
        dbnv_food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':"Dinner Briyani Non Veg"})
        dsv_food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':"Dinner Special Veg"})
        dsnv_food_scan = frappe.db.count('Food Scan',{'date':current_date,'food':"Dinner Special Non Veg"})
        total_dinner_actual = dn_food_scan + dbv_food_scan + dbnv_food_scan + dsv_food_scan + dsnv_food_scan
        dn_gap = dn_head_count -  dn_food_scan
        dbv_gap = dbv_head_count -  dbv_food_scan
        dbnv_gap = dbnv_head_count -  dbnv_food_scan  
        dsv_gap = dsv_head_count -  dsv_food_scan
        dsnv_gap = lsnv_head_count -  dsnv_food_scan
        total_dinner_gap = dn_gap + dbv_gap + dbv_gap + dsv_gap + dsnv_gap
        if total_dinner_plan:
            dn_actual_percent = round(flt((total_dinner_actual / total_dinner_plan) * 100),2)
            dn_gap_percent = round(flt((total_dinner_gap / total_dinner_plan) * 100),2)

    elif food_type == 'Supper':
        sp_head_count = frappe.db.get_value('Food Plan',{'date':add_days(current_date,-1)},'sp_head_count')
        sd_head_count = frappe.db.get_value('Food Plan',{'date':add_days(current_date,-1)},'sd_head_count')
        ssf_head_count = frappe.db.get_value('Food Plan',{'date':add_days(current_date,-1)},'ssf_head_count')
        total_supper_plan = sp_head_count + sd_head_count + ssf_head_count
        sp_food_scan = frappe.db.count('Food Scan',{'date':add_days(current_date,-1),'food':"Supper"}) 
        sd_food_scan = frappe.db.count('Food Scan',{'date':add_days(current_date,-1),'food':"Supper Dates"}) 
        ssf_food_scan = frappe.db.count('Food Scan',{'date':add_days(current_date,-1),'food':"Supper Special Food"}) 
        total_supper_actual = sp_food_scan + sd_food_scan + ssf_food_scan
        sp_gap = sp_head_count - sp_food_scan
        sd_gap = sd_head_count - sd_food_scan
        ssf_gap = ssf_head_count - ssf_food_scan
        total_supper_gap = sp_gap + sd_gap + ssf_gap
        if total_supper_plan:
            sp_actual_percent = round(flt((total_supper_actual / total_supper_plan) * 100),2)
            sp_gap_percent = round(flt((total_supper_gap / total_supper_plan) * 100),2)
       
    else:
        food_type = 'NA' 
    if food_type == 'Supper':
        food_scan_list = frappe.db.get_all('Food Scan',{'date':add_days(current_date,-1),'meal_type':food_type},['id','name1','cdepartment',],limit = 10) 
    else:       
        food_scan_list = frappe.db.get_all('Food Scan',{'date':current_date,'meal_type':food_type},['id','name1','cdepartment',],limit = 10)   
    data.update({
        "current_datetime":current_datetime,
        "food_type": food_type,
        "bf_head_count":bf_head_count,
        "total_breakfast_plan":total_breakfast_plan,
        "bf_food_scan":bf_food_scan,
        "total_breakfast_actual":total_breakfast_actual,
        "bf_gap":bf_gap,
        "total_bf_gap":total_bf_gap,
        "bf_actual_percent":bf_actual_percent,
        "bf_gap_percent": bf_gap_percent,
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
        "lu_actual_percent":lu_actual_percent,
        "lu_gap_percent":lu_gap_percent,
        "dn_head_count":dn_head_count,
        "dbv_head_count":dbv_head_count,
        "dbnv_head_count":dbnv_head_count,
        "dsv_head_count":dsv_head_count,
        "dsnv_head_count":dsnv_head_count,
        "total_dinner_plan":total_dinner_plan,
        "dn_food_scan":dn_food_scan,
        "dbv_food_scan":dbv_food_scan,
        "dbnv_food_scan":dbnv_food_scan,
        "dsv_food_scan":dsv_food_scan,
        "dsnv_food_scan":dsnv_food_scan,
        "total_dinner_actual":total_dinner_actual,
        "dn_gap":dn_gap,
        "dbv_gap":dbv_gap,
        "dbnv_gap":dbnv_gap,
        "dsv_gap":dsv_gap,
        "dsnv_gap":dsnv_gap,
        "total_dinner_gap":total_dinner_gap,
        "dn_actual_percent":dn_actual_percent,
        "dn_gap_percent":dn_gap_percent,
        "sp_head_count":sp_head_count,
        "sd_head_count":sd_head_count,
        "ssf_head_count":ssf_head_count,
        "total_supper_plan":total_supper_plan,
        "sp_food_scan":sp_food_scan,
        "sd_food_scan":sd_food_scan,
        "ssf_food_scan":ssf_food_scan,
        "total_supper_actual":total_supper_actual,
        "sp_gap":sp_gap,
        "sd_gap":sd_gap,
        "ssf_gap":ssf_gap,
        "total_supper_gap":total_supper_gap,
        "sp_actual_percent":sp_actual_percent,
        "sp_gap_percent":sp_gap_percent,
        "food_scan_list":food_scan_list
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
    bf_min_time = frappe.db.get_single_value('Canteen Settings','bf_min_time')
    bf_max_time = frappe.db.get_single_value('Canteen Settings','bf_max_time')
    lu_min_time = frappe.db.get_single_value('Canteen Settings','lu_min_time')
    lu_max_time = frappe.db.get_single_value('Canteen Settings','lu_max_time')
    dn_min_time = frappe.db.get_single_value('Canteen Settings','dn_min_time')
    dn_max_time = frappe.db.get_single_value('Canteen Settings','dn_max_time')
    su_min_time = frappe.db.get_single_value('Canteen Settings','su_min_time')
    su_max_time = frappe.db.get_single_value('Canteen Settings','su_max_time')

    bf_min = datetime.strptime(str(bf_min_time),'%H:%M:%S').time()
    bf_max = datetime.strptime(str(bf_max_time),'%H:%M:%S').time()
    lu_min = datetime.strptime(str(lu_min_time),'%H:%M:%S').time()
    lu_max = datetime.strptime(str(lu_max_time),'%H:%M:%S').time()
    dn_min = datetime.strptime(str(dn_min_time),'%H:%M:%S').time()
    dn_max = datetime.strptime(str(dn_max_time),'%H:%M:%S').time()
    su_min = datetime.strptime(str(su_min_time),'%H:%M:%S').time()
    su_max = datetime.strptime(str(su_max_time),'%H:%M:%S').time()

    break_fast_time = [time(hour=bf_min.hour, minute=bf_min.minute, second=bf_min.second),time(hour=bf_max.hour, minute=bf_max.minute, second=bf_max.second)]
    lunch_time = [time(hour=lu_min.hour, minute=lu_min.minute, second=lu_min.second),time(hour=lu_max.hour, minute=lu_max.minute, second=lu_max.second)]
    dinner_lunch = [time(hour=dn_min.hour, minute=dn_min.minute, second=dn_min.second),time(hour=dn_max.hour, minute=dn_max.minute, second=dn_max.second)]
    supper_time = [time(hour=su_min.hour, minute=su_min.minute, second=su_min.second),time(hour=su_max.hour, minute=su_max.minute, second=su_max.second)]
    curtime = time(hour=nowtime.hour, minute=nowtime.minute, second=nowtime.second)
    food_type = 'NA'
    if is_between(curtime,break_fast_time):
        food_type = 'Break Fast'
    if is_between(curtime,lunch_time):
        food_type = 'Lunch'
    if is_between(curtime,dinner_lunch):
        food_type = 'Dinner'
    if is_between(curtime,supper_time):
        food_type = 'Supper'
    return food_type 
