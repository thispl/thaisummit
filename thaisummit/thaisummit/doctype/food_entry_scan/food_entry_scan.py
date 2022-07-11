# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

from datetime import datetime
import json
import re
import frappe
from frappe.model.document import Document
from frappe.utils import cstr

class FoodEntryScan(Document):
    pass

@frappe.whitelist()
def get_canteen_user_id(user,cur_date):
    employee = frappe.db.exists('Employee',{'status':'Active','employee_number':user})
    guest_entry = frappe.db.exists('Guest Entry',{'name':user})
    # data = ''
    food_type = 'NA'
    if employee:
        emp  = frappe.db.get_value('Employee',employee,['first_name','department','designation'])
        food_type = get_food_time()
        food_scan = frappe.db.exists('Food Scan',{'id':user,'date':cur_date,'food':food_type})
        if food_scan:
            frappe.throw('Employee %s Already scanned for this Meal Time' % emp[0])
        else:
            if food_type == 'Break Fast':
                new_food_scan = frappe.new_doc('Food Scan')
                new_food_scan.id = user
                new_food_scan.name1 = emp[0]
                new_food_scan.cdepartment = emp[1]
                new_food_scan.food = food_type
                new_food_scan.type = ''  
                new_food_scan.party_name = ''
                new_food_scan.tsa_id = ''
                new_food_scan.employee_name = ''
                new_food_scan.department = ''
                new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                new_food_scan.save(ignore_permissions=True)
                frappe.db.commit()
            elif food_type == 'Lunch':
                food_plan = frappe.db.exists('Food Plan',{'date':cur_date})
                if food_plan:
                    meal_type = frappe.db.get_value('Food Plan',{'name':food_plan},['lu_head_count','lbv_head_count','lsv_head_count'])
                    if meal_type[0] > 0:
                        new_food_scan = frappe.new_doc('Food Scan')
                        new_food_scan.id = user
                        new_food_scan.name1 = emp[0]
                        new_food_scan.cdepartment = emp[1]
                        new_food_scan.food = "Lunch"
                        new_food_scan.type = ''  
                        new_food_scan.party_name = ''
                        new_food_scan.tsa_id = ''
                        new_food_scan.employee_name = ''
                        new_food_scan.department = ''
                        new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                        new_food_scan.save(ignore_permissions=True)
                        frappe.db.commit()
                    elif meal_type[1] > 0:
                        emp_menu_pre = frappe.db.exists('Employee Menu Preference',{'employee':user,'date':cur_date,'meal_type':food_type})  
                        if emp_menu_pre:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Lunch Briyani Veg"
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                        else:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Lunch Briyani Non Veg"
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                    elif meal_type [2] > 0:
                        emp_menu_pre = frappe.db.exists('Employee Menu Preference',{'employee':user,'date':cur_date,'meal_type':food_type}) 
                        if emp_menu_pre:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Lunch Special Veg"
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                        else:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Lunch Special Non Veg"
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                    else:
                        new_food_scan = frappe.new_doc('Food Scan')
                        new_food_scan.id = user
                        new_food_scan.name1 = emp[0]
                        new_food_scan.cdepartment = emp[1]
                        new_food_scan.food = food_type
                        new_food_scan.type = ''  
                        new_food_scan.party_name = ''
                        new_food_scan.tsa_id = ''
                        new_food_scan.employee_name = ''
                        new_food_scan.department = ''
                        new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                        new_food_scan.save(ignore_permissions=True)
                        frappe.db.commit()
                else:
                    new_food_scan = frappe.new_doc('Food Scan')
                    new_food_scan.id = user
                    new_food_scan.name1 = emp[0]
                    new_food_scan.cdepartment = emp[1]
                    new_food_scan.food = food_type
                    new_food_scan.type = ''  
                    new_food_scan.party_name = ''
                    new_food_scan.tsa_id = ''
                    new_food_scan.employee_name = ''
                    new_food_scan.department = ''
                    new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                    new_food_scan.save(ignore_permissions=True)
                    frappe.db.commit()
                         
            elif food_type == 'Dinner':
                food_plan = frappe.db.exists('Food Plan',{'date':cur_date})
                if food_plan:
                    meal_type = frappe.db.get_value('Food Plan',{'name':food_plan},['dn_head_count','dbv_head_count','dsv_head_count'])
                    if meal_type [0] > 0:
                        new_food_scan = frappe.new_doc('Food Scan')
                        new_food_scan.id = user
                        new_food_scan.name1 = emp[0]
                        new_food_scan.cdepartment = emp[1]
                        new_food_scan.food = "Dinner"
                        new_food_scan.type = ''  
                        new_food_scan.party_name = ''
                        new_food_scan.tsa_id = ''
                        new_food_scan.employee_name = ''
                        new_food_scan.department = ''
                        new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                        new_food_scan.save(ignore_permissions=True)
                        frappe.db.commit()
                    elif meal_type [1] > 0:
                        emp_menu_pre = frappe.db.exists('Employee Menu Preference',{'employee':user,'date':cur_date,'meal_type':food_type})
                        if emp_menu_pre:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Dinner Briyani Veg"
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                        else:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Dinner Briyani Non Veg"
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                    elif meal_type[2] > 0:
                        emp_menu_pre = frappe.db.exists('Employee Menu Preference',{'employee':user,'date':cur_date,'meal_type':food_type})
                        if emp_menu_pre:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Dinner Special Veg"
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                        else:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Dinner Special Non Veg"
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                    else:
                        new_food_scan = frappe.new_doc('Food Scan')
                        new_food_scan.id = user
                        new_food_scan.name1 = emp[0]
                        new_food_scan.cdepartment = emp[1]
                        new_food_scan.food = "Dinner"
                        new_food_scan.type = ''  
                        new_food_scan.party_name = ''
                        new_food_scan.tsa_id = ''
                        new_food_scan.employee_name = ''
                        new_food_scan.department = ''
                        new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                        new_food_scan.save(ignore_permissions=True)
                        frappe.db.commit()
            elif food_type == 'Supper':
                food_plan = frappe.db.exists('Food Plan',{'date':cur_date})
                if food_plan:
                    meal_type = frappe.db.get_value('Food Plan',{'name':food_plan},['sf_head_count','ssf_head_count','supper'])
                    if meal_type [0] > 0:
                        emp_menu_pre = frappe.db.exists('Employee Menu Preference',{'employee':user,'date':cur_date,'meal_type':food_type})
                        if emp_menu_pre:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Supper Dates"
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                        else:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Supper"
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                    elif meal_type [0] > 0:
                        emp_menu_pre = frappe.db.exists('Employee Menu Preference',{'employee':user,'date':cur_date,'meal_type':food_type})
                        if emp_menu_pre:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Supper Special Food"
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                        else:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Supper"
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                    else:
                        new_food_scan = frappe.new_doc('Food Scan')
                        new_food_scan.id = user
                        new_food_scan.name1 = emp[0]
                        new_food_scan.cdepartment = emp[1]
                        new_food_scan.food = "Supper"
                        new_food_scan.type = ''
                        new_food_scan.party_name = ''
                        new_food_scan.tsa_id = ''
                        new_food_scan.employee_name = ''
                        new_food_scan.department = ''
                        new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                        new_food_scan.save(ignore_permissions=True)
                        frappe.db.commit()
                else:
                    new_food_scan = frappe.new_doc('Food Scan')
                    new_food_scan.id = user
                    new_food_scan.name1 = emp[0]
                    new_food_scan.cdepartment = emp[1]
                    new_food_scan.food = "Supper"
                    new_food_scan.type = ''
                    new_food_scan.party_name = ''
                    new_food_scan.tsa_id = ''
                    new_food_scan.employee_name = ''
                    new_food_scan.department = ''
                    new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                    new_food_scan.save(ignore_permissions=True)
                    frappe.db.commit()
            else: 
                frappe.throw('No Food Allowed this Time')      
            
    elif guest_entry:
        guest_entry_list = frappe.db.get_value('Guest Entry',guest_entry,['type','customer_name','party_name'])
        food_type = get_food_time()
        from_date = frappe.db.get_value('Guest Entry',guest_entry,'from')
        to_date = frappe.db.get_value('Guest Entry',guest_entry,'to')
        str_to_date = datetime.strptime(str(cur_date),'%Y-%m-%d').date()
        if str_to_date >= from_date and str_to_date <= to_date:
            allowed_items = frappe.get_value('Guest Entry',{'name':guest_entry},['allowed_items'])
            # Converting string to list
            allowed_items = allowed_items.replace("'","")
            allowed_items = allowed_items.strip('][').split(', ')
            if cstr(food_type) in allowed_items:
                frappe.errprint('yes')
                food_scan = frappe.db.exists('Food Scan',{'id':guest_entry,'date':cur_date,'food':food_type})
                
                if food_scan:
                    frappe.throw('Guest User %s Already scanned for this Meal Time' % guest_entry)
                else:
                    frappe.errprint('GuestEntry')
                    ge = frappe.get_doc('Guest Entry',guest_entry)
                    new_food_scan = frappe.new_doc('Food Scan')
                    new_food_scan.id = ge.name
                    new_food_scan.name1 = ''
                    new_food_scan.cdepartment = ''
                    new_food_scan.food = food_type
                    new_food_scan.type = ge.type
                    new_food_scan.party_name = ge.party_name
                    new_food_scan.tsa_id = ge.requester_id
                    new_food_scan.employee_name = ge.employee_name
                    new_food_scan.department = ge.department
                    new_food_scan.price = frappe.db.get_value('Food Menu',{'name':get_food_time()},['price'])
                    new_food_scan.save(ignore_permissions=True)
                    frappe.db.commit()
            else:
                frappe.throw('You are not allowed for this Meal %s' % food_type)        
        else:
            frappe.throw('You are not allowed to punch in Canteen Today')   
        # return data    
    else:
        frappe.throw('User has no Entry')

    return "Completed"

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

# @frappe.whitelist()
# def live_screen_view(date):
#     food_type = get_food_time()
#     current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")
#     if food_type == 'Break Fast':
#         food_plan = frappe.db.get_value('Food Plan',{'date':date},['bf_head_count'])
#         food_scan = frappe.db.get_value('Food Scan',{'date':date,'food':food_type})

#     data = ''
#     data = "<table class='table table-bordered=1 >"
#     data += "<tr><td style ='background-color:#90ee90'></td><td colspan='7' style='background-color:#90ee90;border:1px solid black'><center style='color:#000000'><b>%s</b></center></td><td colspan='2' style='background-color:#90ee90;border:1px solid black'><center style='color:#000000'><b>%s</b></center></td></tr>"%(current_datetime,food_type)
#     data += "<th colspan='1' style='background-color:#90ee90;border:1px solid black'><center style='color:#000000'>LIST</center></th><th  colspan='1' style='background-color:#90ee90;border:1px solid black'><center style='color:#000000'>NORMAL</center></th><th  colspan='1' style='background-color:#90ee90;border:1px solid black'><center style='color:#000000'>S(VEG)</center></th><th  colspan='1' style='background-color:#90ee90;border:1px solid black'><center style='color:#000000'>S(N-VEG)</center></th><th  colspan='1' style='background-color:#90ee90;border:1px solid black'><center style='color:#000000'>B(VEG)</center></th><th  colspan='1' style='background-color:#90ee90;border:1px solid black'><center style='color:#000000'>B(N-VEG)</center></th><th  colspan='1' style='background-color:#90ee90;border:1px solid black'><center style='color:#000000'>TOTAL</center></th><th colspan='2' style='background-color:#90ee90;border:1px solid black'><center style='color:#000000'><b>%</b></center></th></tr>"
#     data += "<td colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>PLAN</center></td><td  colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>20</center></td><td  colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>30</center></td><td  colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>40</center></td><td colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>50</center></td><td  colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>60</center></td><td  colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>100</center></td><td  colspan='2' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>100%</center></td></tr>"
#     data += "<td colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>ACTUAL</center></td><td  colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>20</center></td><td  colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>30</center></td><td  colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>40</center></td><td colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>50</center></td><td  colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>60</center></td><td  colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>100</center></td><td  colspan='2' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>100%</center></td></tr>"
#     data += "<td colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>GAP</center></td><td  colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>20</center></td><td  colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>30</center></td><td  colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>40</center></td><td colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>50</center></td><td  colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>60</center></td><td  colspan='1' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>100</center></td><td  colspan='2' style='background-color:#FFFFFF;border:1px solid black'><center style='color:#000000'>100%</center></td></tr>"
#     data += "</table>"
    
#     return data
   
    