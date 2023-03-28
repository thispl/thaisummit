# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

from datetime import datetime
import frappe
from frappe import _, msgprint
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day,add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date

def execute(filters=None):
    columns,data = [],[]
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
    columns = [
        _('Doc No') +':Data:100',_('Date') +':Data:100',_('Meal Type') +':Data:100',_('Plan Head Count') +':Data:100',_('Party Name') +':Data:100',
        _('Requester ID') +':Data:100',_('Requester Name') +':Data:100',_('Requester Department') +':Data:100'
    ]
    return columns
    

def get_data(filters):
    data = []
    dates = get_dates(filters.from_date,filters.to_date)
    for date in dates:
        if filters.menu:
            food_scan = frappe.db.get_all('Food Scan',{'date':date,'food':filters.menu},['name','id','food','party_name','tsa_id','employee_name','department'])
        if not filters.menu:
            food_scan = frappe.db.get_all('Food Scan',{'date':date,},['name','id','food','party_name','tsa_id','employee_name','department'])
        for food in food_scan:
            if food.food == 'Break Fast':
                if food.party_name:
                    bf_count = frappe.db.get_value('Food Plan',{'date':date},['bf_head_count'])
                    row1 = [food.name,date,food.food,bf_count,food.party_name,food.tsa_id,food.employee_name,food.department]
                    data.append(row1)
                    
            if food.food == 'Lunch':
                if food.party_name:
                    lu_count = frappe.db.get_value('Food Plan',{'date':date},['lu_head_count'])
                    row2 = [food.name,date,food.food,lu_count,food.party_name,food.tsa_id,food.employee_name,food.department]
                    data.append(row2)    
        
            if food.food == 'Lunch Briyani Veg':
                if food.party_name:
                    lbv_count = frappe.db.get_value('Food Plan',{'date':date},['lbv_head_count'])
                    row3 = [food.name,date,food.food,lbv_count,food.party_name,food.tsa_id,food.employee_name,food.department]
                    data.append(row3)

            if food.food == 'Lunch Briyani Non Veg':
                if food.party_name:
                    lbnv_count = frappe.db.get_value('Food Plan',{'date':date},['lbnv_head_count'])
                    row4 = [food.name,date,food.food,lbnv_count,food.party_name,food.tsa_id,food.employee_name,food.department]
                    data.append(row4)

            if food.food == 'Lunch Special Veg':
                if food.party_name:
                    lsv_count = frappe.db.get_value('Food Plan',{'date':date},['lsv_head_count'])
                    row5 = [food.name,date,food.food,lsv_count,food.party_name,food.tsa_id,food.employee_name,food.department]
                    data.append(row5)

            if food.food == 'Lunch Special Non Veg':
                if food.party_name:
                    lsnv_count = frappe.db.get_value('Food Plan',{'date':date},['lsnv_head_count'])
                    row6 = [food.name,date,food.food,lsnv_count,food.party_name,food.tsa_id,food.employee_name,food.department]
                    data.append(row6)

            if food.food == 'Dinner':
                if food.party_name:
                    dn_count = frappe.db.get_value('Food Plan',{'date':date},['dn_head_count'])
                    row7 = [food.name,date,food.food,dn_count,food.party_name,food.tsa_id,food.employee_name,food.department]
                    data.append(row7)

            if food.food == 'Dinner Briyani Veg':
                if food.party_name:
                    dbv_count = frappe.db.get_value('Food Plan',{'date':date},['dbv_head_count'])
                    row8 = [food.name,date,food.food,dbv_count,food.party_name,food.tsa_id,food.employee_name,food.department]
                    data.append(row8)

            if food.food == 'Dinner Briyani Non Veg':
                if food.party_name:
                    dbnv_count = frappe.db.get_value('Food Plan',{'date':date},['dbnv_head_count'])
                    row9 = [food.name,date,food.food,dbnv_count,food.party_name,food.tsa_id,food.employee_name,food.department]
                    data.append(row9)

            if food.food == 'Dinner Special Veg':
                if food.party_name:
                    dsv_count = frappe.db.get_value('Food Plan',{'date':date},['dsv_head_count'])
                    row10 = [food.name,date,food.food,dsv_count,food.party_name,food.tsa_id,food.employee_name,food.department]
                    data.append(row10)

            if food.food == 'Dinner Special Non Veg':
                if food.party_name:
                    dsnv_count = frappe.db.get_value('Food Plan',{'date':date},['dsnv_head_count'])
                    row11 = [food.name,date,food.food,dsnv_count,food.party_name,food.tsa_id,food.employee_name,food.department]
                    data.append(row11)

            if food.food == 'Supper':
                if food.party_name:
                    sp_count = frappe.db.get_value('Food Plan',{'date':date},['sp_head_count'])
                    row12 = [food.name,date,food.food,sp_count,food.party_name,food.tsa_id,food.employee_name,food.department]
                    data.append(row12)

            if food.food == 'Supper Dates':
                if food.party_name:
                    sd_count = frappe.db.get_value('Food Plan',{'date':date},['sd_head_count'])
                    row13 = [food.name,date,food.food,sd_count,food.party_name,food.tsa_id,food.employee_name,food.department]
                    data.append(row13)

            if food.food == 'Supper Special Food':
                if food.party_name:
                    ssf_count = frappe.db.get_value('Food Plan',{'date':date},['ssf_head_count'])
                    row14 = [food.name,date,food.food,ssf_count,food.party_name,food.tsa_id,food.employee_name,food.department]
                    data.append(row14)
    return data




def get_dates(from_date,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates

