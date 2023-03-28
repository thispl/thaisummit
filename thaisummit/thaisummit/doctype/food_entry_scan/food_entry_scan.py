# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

from datetime import datetime
from genericpath import exists
import json
import re
import frappe
from frappe.model.document import Document
from frappe.utils import cstr
from frappe.utils.data import add_days, today

class FoodEntryScan(Document):
    pass

@frappe.whitelist()
def get_canteen_user_id(user):
    cur_date = datetime.now().date()
    employee = frappe.db.exists('Employee',{'status':'Active','employee_number':user})
    guest_entry = frappe.db.exists('Guest Entry',{'name':user})
    # data = ''
    food_type = 'NA'
    if employee:
        emp  = frappe.db.get_value('Employee',employee,['first_name','department','designation'])
        food_type = get_food_time()
        previous_food_scan = frappe.db.exists('Food Scan',{'id':user,'date':add_days(cur_date,-1),'meal_type':food_type})
        food_scan = frappe.db.exists('Food Scan',{'id':user,'date':cur_date,'meal_type':food_type})
        if food_scan:
            frappe.db.set_value('Food Entry Scan','employee_guest','')
            frappe.msgprint('Employee %s Already scanned for this Meal Time' % emp[0])
        elif previous_food_scan and food_type == 'Supper':
            frappe.db.set_value('Food Entry Scan','employee_guest','')
            frappe.msgprint('Employee %s Already scanned for this Meal Time' % emp[0])
        else:
            if food_type == 'Break Fast':
                food_plan = frappe.db.exists('Food Plan',{'date':cur_date})
                new_food_scan = frappe.new_doc('Food Scan')
                new_food_scan.id = user
                new_food_scan.date = cur_date
                new_food_scan.name1 = emp[0]
                new_food_scan.cdepartment = emp[1]
                new_food_scan.food = 'Break Fast'
                new_food_scan.type = ''
                new_food_scan.meal_type = 'Break Fast'
                new_food_scan.party_name = ''
                new_food_scan.tsa_id = ''
                new_food_scan.employee_name = ''
                new_food_scan.department = ''
                new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['bf_price'])
                qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                if qr_checkin:
                    emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                    new_food_scan.cost_centre = emp 
                elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                    new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                else:
                    new_food_scan.cost_centre = ''
                new_food_scan.save(ignore_permissions=True)
                frappe.db.commit()
                
            elif food_type == 'Lunch':
                food_plan = frappe.db.exists('Food Plan',{'date':cur_date})
                if food_plan:
                    meal_type = frappe.db.get_value('Food Plan',{'name':food_plan},['lu_head_count','lbv_head_count','lsv_head_count'])
                    if meal_type[0] > 0:
                        new_food_scan = frappe.new_doc('Food Scan')
                        new_food_scan.date = cur_date
                        new_food_scan.id = user
                        new_food_scan.name1 = emp[0]
                        new_food_scan.cdepartment = emp[1]
                        new_food_scan.food = "Lunch"
                        new_food_scan.meal_type = 'Lunch'
                        new_food_scan.type = ''  
                        new_food_scan.party_name = ''
                        new_food_scan.tsa_id = ''
                        new_food_scan.employee_name = ''
                        new_food_scan.department = ''
                        new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['lu_price'])
                        qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                        if qr_checkin:
                            emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            new_food_scan.cost_centre = emp 
                        elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                            new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                        else:
                            new_food_scan.cost_centre = ''
                        new_food_scan.save(ignore_permissions=True)
                        frappe.db.commit()
                    elif meal_type[1] > 0:
                        emp_menu_pre = frappe.db.exists('Employee Menu Preference',{'employee':user,'date':cur_date,'meal_type':"Lunch Briyani Veg"})  
                        employee = frappe.db.exists('Employee',{'status':'Active','employee':user,'meal_type':1})
                        if emp_menu_pre:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.date = cur_date
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Lunch Briyani Veg"
                            new_food_scan.meal_type = 'Lunch'
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['lbv_price'])
                            qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                            if qr_checkin:
                                emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                                new_food_scan.cost_centre = emp 
                            elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                                new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            else:
                                new_food_scan.cost_centre = ''
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()

                        elif employee:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.date = cur_date
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Lunch Briyani Veg"
                            new_food_scan.meal_type = 'Lunch'
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['lbv_price'])
                            qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                            if qr_checkin:
                                emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                                new_food_scan.cost_centre = emp 
                            elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                                new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            else:
                                new_food_scan.cost_centre = ''
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                        else:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.date = cur_date
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Lunch Briyani Non Veg"
                            new_food_scan.meal_type = 'Lunch'
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['lbnv_price'])
                            qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                            if qr_checkin:
                                emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                                new_food_scan.cost_centre = emp 
                            elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                                new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            else:
                                new_food_scan.cost_centre = ''
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                    elif meal_type [2] > 0:
                        emp_menu_pre = frappe.db.exists('Employee Menu Preference',{'employee':user,'date':cur_date,'meal_type':"Lunch Special Veg"}) 
                        employee = frappe.db.exists('Employee',{'status':'Active','employee':user,'meal_type':1})
                        if emp_menu_pre:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.date = cur_date
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Lunch Special Veg"
                            new_food_scan.meal_type = 'Lunch'
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['lsv_price'])
                            qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                            if qr_checkin:
                                emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                                new_food_scan.cost_centre = emp 
                            elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                                new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            else:
                                new_food_scan.cost_centre = ''
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                        elif employee:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.date = cur_date
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Lunch Special Veg"
                            new_food_scan.meal_type = 'Lunch'
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['lsv_price'])
                            qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                            if qr_checkin:
                                emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                                new_food_scan.cost_centre = emp 
                            elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                                new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            else:
                                new_food_scan.cost_centre = ''
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()

                        else:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.date = cur_date
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Lunch Special Non Veg"
                            new_food_scan.meal_type = 'Lunch'
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['lsnv_price'])
                            qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                            if qr_checkin:
                                emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                                new_food_scan.cost_centre = emp 
                            elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                                new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            else:
                                new_food_scan.cost_centre = ''
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                    else:
                        new_food_scan = frappe.new_doc('Food Scan')
                        new_food_scan.id = user
                        new_food_scan.date = cur_date
                        new_food_scan.name1 = emp[0]
                        new_food_scan.cdepartment = emp[1]
                        new_food_scan.food = 'Lunch'
                        new_food_scan.meal_type = 'Lunch'
                        new_food_scan.type = ''  
                        new_food_scan.party_name = ''
                        new_food_scan.tsa_id = ''
                        new_food_scan.employee_name = ''
                        new_food_scan.department = ''
                        new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['lu_price'])
                        qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                        if qr_checkin:
                            emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            new_food_scan.cost_centre = emp 
                        elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                            new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                        else:
                            new_food_scan.cost_centre = ''
                        new_food_scan.save(ignore_permissions=True)
                        frappe.db.commit()
                else:
                    new_food_scan = frappe.new_doc('Food Scan')
                    new_food_scan.id = user
                    new_food_scan.date = cur_date
                    new_food_scan.name1 = emp[0]
                    new_food_scan.cdepartment = emp[1]
                    new_food_scan.food = 'Lunch'
                    new_food_scan.meal_type = 'Lunch'
                    new_food_scan.type = ''  
                    new_food_scan.party_name = ''
                    new_food_scan.tsa_id = ''
                    new_food_scan.employee_name = ''
                    new_food_scan.department = ''
                    new_food_scan.price = frappe.db.get_value('Food plan',{'name':food_plan},['lu_price'])
                    qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                    if qr_checkin:
                        emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                        new_food_scan.cost_centre = emp 
                    elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                        new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                    else:
                        new_food_scan.cost_centre = ''
                    new_food_scan.save(ignore_permissions=True)
                    frappe.db.commit()
                         
            elif food_type == 'Dinner':
                food_plan = frappe.db.exists('Food Plan',{'date':cur_date})
                if food_plan:
                    meal_type = frappe.db.get_value('Food Plan',{'name':food_plan},['dn_head_count','dbv_head_count','dsv_head_count'])
                    if meal_type [0] > 0:
                        new_food_scan = frappe.new_doc('Food Scan')
                        new_food_scan.id = user
                        new_food_scan.date = cur_date
                        new_food_scan.name1 = emp[0]
                        new_food_scan.cdepartment = emp[1]
                        new_food_scan.food = "Dinner"
                        new_food_scan.meal_type = 'Dinner'
                        new_food_scan.type = ''  
                        new_food_scan.party_name = ''
                        new_food_scan.tsa_id = ''
                        new_food_scan.employee_name = ''
                        new_food_scan.department = ''
                        new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['dn_price'])
                        qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                        if qr_checkin:
                            emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            new_food_scan.cost_centre = emp 
                        elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                            new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                        else:
                            new_food_scan.cost_centre = ''
                        new_food_scan.save(ignore_permissions=True)
                        frappe.db.commit()
                    elif meal_type [1] > 0:
                        emp_menu_pre = frappe.db.exists('Employee Menu Preference',{'employee':user,'date':cur_date,'meal_type':"Dinner Briyani Veg"})
                        employee = frappe.db.exists('Employee',{'status':'Active','employee':user,'meal_type':1})
                        if emp_menu_pre:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.date = cur_date
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Dinner Briyani Veg"
                            new_food_scan.meal_type = 'Dinner'
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['dbv_price'])
                            qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                            if qr_checkin:
                                emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                                new_food_scan.cost_centre = emp 
                            elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                                new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            else:
                                new_food_scan.cost_centre = ''
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                        elif employee:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.date = cur_date
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Dinner Briyani Veg"
                            new_food_scan.meal_type = 'Dinner'
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['dbv_price'])
                            qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                            if qr_checkin:
                                emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                                new_food_scan.cost_centre = emp 
                            elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                                new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            else:
                                new_food_scan.cost_centre = ''
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()

                        else:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.date = cur_date
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Dinner Briyani Non Veg"
                            new_food_scan.meal_type = 'Dinner'
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['dbnv_price'])
                            qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                            if qr_checkin:
                                emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                                new_food_scan.cost_centre = emp 
                            elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                                new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            else:
                                new_food_scan.cost_centre = ''
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                    elif meal_type[2] > 0:
                        emp_menu_pre = frappe.db.exists('Employee Menu Preference',{'employee':user,'date':cur_date,'meal_type':"Dinner Special Veg"})
                        employee = frappe.db.exists('Employee',{'status':'Active','employee':user,'meal_type':1})
                        if emp_menu_pre:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.date = cur_date
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Dinner Special Veg"
                            new_food_scan.meal_type = 'Dinner'
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['dsv_price'])
                            qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                            if qr_checkin:
                                emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                                new_food_scan.cost_centre = emp 
                            elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                                new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            else:
                                new_food_scan.cost_centre = ''
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                        elif employee:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.date = cur_date
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Dinner Special Veg"
                            new_food_scan.meal_type = 'Dinner'
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['dsv_price'])
                            qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                            if qr_checkin:
                                emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                                new_food_scan.cost_centre = emp 
                            elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                                new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            else:
                                new_food_scan.cost_centre = ''
                            new_food_scan.save(ignore_permissions=True)
                        else:
                            new_food_scan = frappe.new_doc('Food Scan')
                            new_food_scan.id = user
                            new_food_scan.date = cur_date
                            new_food_scan.name1 = emp[0]
                            new_food_scan.cdepartment = emp[1]
                            new_food_scan.food = "Dinner Special Non Veg"
                            new_food_scan.meal_type = 'Dinner'
                            new_food_scan.type = ''  
                            new_food_scan.party_name = ''
                            new_food_scan.tsa_id = ''
                            new_food_scan.employee_name = ''
                            new_food_scan.department = ''
                            new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['dsnv_price'])
                            qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                            if qr_checkin:
                                emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                                new_food_scan.cost_centre = emp 
                            elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                                new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            else:
                                new_food_scan.cost_centre = ''
                            new_food_scan.save(ignore_permissions=True)
                            frappe.db.commit()
                    else:
                        new_food_scan = frappe.new_doc('Food Scan')
                        new_food_scan.id = user
                        new_food_scan.date = cur_date
                        new_food_scan.name1 = emp[0]
                        new_food_scan.cdepartment = emp[1]
                        new_food_scan.food = "Dinner"
                        new_food_scan.meal_type = 'Dinner'
                        new_food_scan.type = ''  
                        new_food_scan.party_name = ''
                        new_food_scan.tsa_id = ''
                        new_food_scan.employee_name = ''
                        new_food_scan.department = ''
                        new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['dn_price'])
                        qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                        if qr_checkin:
                            emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            new_food_scan.cost_centre = emp 
                        elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                            new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                        else:
                            new_food_scan.cost_centre = ''
                        new_food_scan.save(ignore_permissions=True)
                        frappe.db.commit()
                else:
                    new_food_scan = frappe.new_doc('Food Scan')
                    new_food_scan.id = user
                    new_food_scan.date = cur_date
                    new_food_scan.name1 = emp[0]
                    new_food_scan.cdepartment = emp[1]
                    new_food_scan.food = "Dinner"
                    new_food_scan.meal_type = 'Dinner'
                    new_food_scan.type = ''  
                    new_food_scan.party_name = ''
                    new_food_scan.tsa_id = ''
                    new_food_scan.employee_name = ''
                    new_food_scan.department = ''
                    new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['dn_price'])
                    qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                    if qr_checkin:
                        emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                        new_food_scan.cost_centre = emp 
                    elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                        new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                    else:
                        new_food_scan.cost_centre = ''
                    new_food_scan.save(ignore_permissions=True)
                    frappe.db.commit()  
                          
            elif food_type == 'Supper':
                food_scan = frappe.db.exists('Food Scan',{'id':user,'date':add_days(cur_date,-1),'meal_type':food_type})
                food_plan = frappe.db.exists('Food Plan',{'date':add_days(cur_date,-1)})
                if food_plan:
                    meal_type = frappe.db.get_value('Food Plan',{'name':food_plan},['sp_head_count','sd_head_count','ssf_head_count',])
                    if meal_type [0] > 0:
                        frappe.errprint(meal_type[0])
                        new_food_scan = frappe.new_doc('Food Scan')
                        new_food_scan.id = user
                        new_food_scan.date = add_days(today(),-1)
                        new_food_scan.name1 = emp[0]
                        new_food_scan.cdepartment = emp[1]
                        new_food_scan.food = "Supper"
                        new_food_scan.meal_type = 'Supper'
                        new_food_scan.type = ''  
                        new_food_scan.party_name = ''
                        new_food_scan.tsa_id = ''
                        new_food_scan.employee_name = ''
                        new_food_scan.department = ''
                        new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['sp_price'])
                        qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                        if qr_checkin:
                            emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            new_food_scan.cost_centre = emp 
                        elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                            new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                        else:
                            new_food_scan.cost_centre = ''
                        new_food_scan.save(ignore_permissions=True)
                        frappe.db.commit()
                    elif meal_type [1] > 0:
                        frappe.errprint(meal_type[1])
                        new_food_scan = frappe.new_doc('Food Scan')
                        new_food_scan.id = user
                        new_food_scan.date = add_days(today(),-1)
                        new_food_scan.name1 = emp[0]
                        new_food_scan.cdepartment = emp[1]
                        new_food_scan.food = "Supper Dates"
                        new_food_scan.meal_type = 'Supper'
                        new_food_scan.type = ''  
                        new_food_scan.party_name = ''
                        new_food_scan.tsa_id = ''
                        new_food_scan.employee_name = ''
                        new_food_scan.department = ''
                        new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['sd_price'])
                        qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                        if qr_checkin:
                            emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            new_food_scan.cost_centre = emp 
                        elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                            new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                        else:
                            new_food_scan.cost_centre = ''
                        new_food_scan.save(ignore_permissions=True)
                        frappe.db.commit()
                    else:
                        frappe.errprint('supper special food')
                        new_food_scan = frappe.new_doc('Food Scan')
                        new_food_scan.id = user
                        new_food_scan.date = add_days(today(),-1)
                        new_food_scan.name1 = emp[0]
                        new_food_scan.cdepartment = emp[1]
                        new_food_scan.food = "Supper Special Food"
                        new_food_scan.meal_type = 'Supper'
                        new_food_scan.type = ''
                        new_food_scan.party_name = ''
                        new_food_scan.tsa_id = ''
                        new_food_scan.employee_name = ''
                        new_food_scan.department = ''
                        new_food_scan.price = frappe.db.get_value('Food Plan',{'name':food_plan},['ssf_price'])
                        qr_checkin = frappe.db.exists('QR Checkin',{'employee_id':user,'shift_date':cur_date})
                        if qr_checkin:
                            emp = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                            new_food_scan.cost_centre = emp 
                        elif frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre']):
                            new_food_scan.cost_centre = frappe.db.get_value('Employee',{'status':'Active','name':user},['cost_centre'])
                        else:
                            new_food_scan.cost_centre = ''
                        new_food_scan.save(ignore_permissions=True)
                        frappe.db.commit()
            else: 
                frappe.db.set_value('Food Entry Scan','employee_guest','')
                frappe.throw('No Food Allowed this Time')      
            
    elif guest_entry:
        guest_entry_list = frappe.db.get_value('Guest Entry',guest_entry,['type','customer_name','party_name'])
        food_type = get_food_time()
        frappe.errprint(food_type)
        food_plan = frappe.db.exists('Food Plan',{'date':cur_date})
        from_date = frappe.db.get_value('Guest Entry',guest_entry,'from')
        to_date = frappe.db.get_value('Guest Entry',guest_entry,'to')
        str_to_date = datetime.strptime(str(cur_date),'%Y-%m-%d').date()
        if str_to_date >= from_date and str_to_date <= to_date:
            allowed_items = frappe.get_value('Guest Entry',{'name':guest_entry},['allowed_items'])
            # Converting string to list
            al_list = stringToList(allowed_items)
            if str(food_type) in al_list:
                food_scan = frappe.db.exists('Food Scan',{'id':guest_entry,'date':cur_date,'food':food_type})
                if food_scan:
                    frappe.db.set_value('Food Entry Scan','employee_guest','')
                    frappe.throw('Guest User %s Already scanned for this Meal Time' % guest_entry)
                else:
                    ge = frappe.get_doc('Guest Entry',guest_entry)
                    new_food_scan = frappe.new_doc('Food Scan')
                    new_food_scan.id = ge.name
                    new_food_scan.date = cur_date
                    new_food_scan.name1 = ''
                    new_food_scan.cdepartment = ''
                    new_food_scan.food = food_type
                    new_food_scan.meal_type = food_type
                    new_food_scan.type = ge.type
                    new_food_scan.party_name = ge.party_name
                    new_food_scan.tsa_id = ge.requester_id
                    new_food_scan.employee_name = ge.employee_name
                    new_food_scan.department = ge.department
                    new_food_scan.price = frappe.db.get_value('Food Menu',{'name':food_plan},['price'])
                    new_food_scan.cost_centre = ''
                    new_food_scan.save(ignore_permissions=True)
                    frappe.db.commit()
            else:
                frappe.db.set_value('Food Entry Scan','employee_guest','')
                frappe.throw('You are not allowed for this Meal %s' % food_type)        
        else:
            frappe.db.set_value('Food Entry Scan','employee_guest','')
            frappe.throw('You are not allowed to punch in Canteen Today')   
        # return data    
    else:
        frappe.throw('User has no Entry')
        frappe.db.set_value('Food Entry Scan','employee_guest','')  

    return "Completed"

def stringToList(string):
    listRes = list(string.split(","))
    return listRes

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
   
    