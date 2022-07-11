from datetime import datetime
import frappe
from frappe import _, msgprint
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date


def execute(filters=None):
    columns,data = [],[]
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    column = [
        _('Date') +':Data:100',
        _('Meal Type') +':Data:200',
        _('Planned Head Count') +':Data:300',
        _('Price') +':Currency:100',
        _('Amount') +':Currency:100',
        ]
    return column

def get_data(filters):
    data = []
    dates = get_dates(filters.from_date,filters.to_date)
    for date in dates:
        if filters.menu:
            food_menu = frappe.db.get_all('Food Menu',{'name':filters.menu},['*'])
        if not filters.menu:
            food_menu = frappe.db.get_all('Food Menu',['*'])
        for menu in food_menu:
            if menu.name == 'Break Fast':
                bf = frappe.db.exists('Food Plan',{'date':date})
                if bf:
                    bf_count = frappe.db.get_value('Food Plan',{'date':date},['bf_head_count'])
                    bf_price = frappe.db.get_value('Food Plan',{'date':date},['bf_price'])
                    bf_amount = frappe.db.get_value('Food Plan',{'date':date},['bf_amount'])
                    row1 = [format_date(date),menu.name,bf_count,bf_price,bf_amount]
                    data.append(row1)
            if menu.name == 'Lunch':
                lu = frappe.db.exists('Food Plan',{'date':date})
                if lu:
                    lu_count = frappe.db.get_value('Food Plan',{'date':date},['lu_head_count'])
                    lu_price = frappe.db.get_value('Food Plan',{'date':date},['lu_price'])
                    lu_amount = frappe.db.get_value('Food Plan',{'date':date},['lu_amount'])
                    row2 = [format_date(date),menu.name,lu_count,lu_price,lu_amount]
                    data.append(row2)
            if menu.name == 'Lunch Briyani Veg':
                lbv = frappe.db.exists('Food Plan',{'date':date})
                if lbv:
                    lbv_count = frappe.db.get_value('Food Plan',{'date':date},['lbv_head_count'])
                    lbv_price = frappe.db.get_value('Food Plan',{'date':date},['lbv_price'])  
                    lbv_amount = frappe.db.get_value('Food Plan',{'date':date},['lbv_amount'])  
                    row3 = [format_date(date),menu.name,lbv_count,lbv_price,lbv_amount]
                    data.append(row3) 
            if menu.name == 'Lunch Briyani Non Veg':
                lbnv = frappe.db.exists('Food Plan',{'date':date})
                if lbnv:
                    lbnv_count = frappe.db.get_value('Food Plan',{'date':date},['lbnv_head_count'])
                    lbnv_price = frappe.db.get_value('Food Plan',{'date':date},['lbnv_price'])  
                    lbnv_amount = frappe.db.get_value('Food Plan',{'date':date},['lbnv_amount'])  
                    row4 = [format_date(date),menu.name,lbnv_count,lbnv_price,lbnv_amount]
                    data.append(row4)
            if menu.name == 'Lunch Special Veg':
                lsv = frappe.db.exists('Food Plan',{'date':date})
                if lsv:
                    lsv_count = frappe.db.get_value('Food Plan',{'date':date},['lsv_head_count'])
                    lsv_price = frappe.db.get_value('Food Plan',{'date':date},['lsv_price'])  
                    lsv_amount = frappe.db.get_value('Food Plan',{'date':date},['lsv_amount'])  
                    row5 = [format_date(date),menu.name,lsv_count,lsv_price,lsv_amount]
                    data.append(row5)
            if menu.name == 'Lunch Special Non Veg':
                lsnv = frappe.db.exists('Food Plan',{'date':date})
                if lsnv:
                    lsnv_count = frappe.db.get_value('Food Plan',{'date':date},['lsnv_head_count'])
                    lsnv_price = frappe.db.get_value('Food Plan',{'date':date},['lsnv_price'])  
                    lsnv_amount = frappe.db.get_value('Food Plan',{'date':date},['lsnv_amount'])  
                    row6 = [format_date(date),menu.name,lsnv_count,lsnv_price,lsnv_amount]
                    data.append(row6)
            if menu.name == 'Dinner':
                dn = frappe.db.exists('Food Plan',{'date':date})
                if dn:
                    dn_count = frappe.db.get_value('Food Plan',{'date':date},['dn_head_count'])
                    dn_price = frappe.db.get_value('Food Plan',{'date':date},['dn_price'])  
                    dn_amount = frappe.db.get_value('Food Plan',{'date':date},['dn_amount'])  
                    row7 = [format_date(date),menu.name,dn_count,dn_price,dn_amount]
                    data.append(row7)
            if menu.name == 'Dinner Briyani Veg':
                dbv = frappe.db.exists('Food Plan',{'date':date})
                if dbv: 
                    dbv_count = frappe.db.get_value('Food Plan',{'date':date},['dbv_head_count'])
                    dbv_price = frappe.db.get_value('Food Plan',{'date':date},['dbv_price'])  
                    dbv_amount = frappe.db.get_value('Food Plan',{'date':date},['dbv_amount'])  
                    row8 = [format_date(date),menu.name,dbv_count,dbv_price,dbv_amount]
                    data.append(row8)  
            if menu.name == 'Dinner Briyani Non Veg':
                dbnv = frappe.db.exists('Food Plan',{'date':date})
                if dbnv: 
                    dbnv_count = frappe.db.get_value('Food Plan',{'date':date},['dbnv_head_count'])
                    dbnv_price = frappe.db.get_value('Food Plan',{'date':date},['dbnv_price'])  
                    dbnv_amount = frappe.db.get_value('Food Plan',{'date':date},['dbnv_amount'])  
                    row9 = [format_date(date),menu.name,dbnv_count,dbnv_price,dbnv_amount]
                    data.append(row9)
            if menu.name == 'Dinner Special Veg':
                dsv = frappe.db.exists('Food Plan',{'date':date})
                if dsv:
                    dsv_count = frappe.db.get_value('Food Plan',{'date':date},['dsv_head_count'])
                    dsv_price = frappe.db.get_value('Food Plan',{'date':date},['dsv_price'])  
                    dsv_amount = frappe.db.get_value('Food Plan',{'date':date},['dsv_amount'])  
                    row10 = [format_date(date),menu.name,dsv_count,dsv_price,dsv_amount]
                    data.append(row10)
            if menu.name == 'Dinner Special Non Veg':
                dsnv = frappe.db.exists('Food Plan',{'date':date})
                if dsnv:
                    dsnv_count = frappe.db.get_value('Food Plan',{'date':date},['dsnv_head_count'])
                    dsnv_price = frappe.db.get_value('Food Plan',{'date':date},['dsnv_price'])  
                    dsnv_amount = frappe.db.get_value('Food Plan',{'date':date},['dsnv_amount'])  
                    row11 = [format_date(date),menu.name,dsnv_count,dsnv_price,dsnv_amount]
                    data.append(row11)
            if menu.name == 'Supper':
                sp = frappe.db.exists('Food Plan',{'date':date})
                if sp:
                    sp_count = frappe.db.get_value('Food Plan',{'date':date},['sp_head_count'])
                    sp_price = frappe.db.get_value('Food Plan',{'date':date},['sp_price'])  
                    sp_amount = frappe.db.get_value('Food Plan',{'date':date},['sp_amount'])  
                    row12 = [format_date(date),menu.name,sp_count,sp_price,sp_amount]
                    data.append(row12)
            if menu.name == 'Supper Dates':
                sd = frappe.db.exists('Food Plan',{'date':date})
                if sd:
                    sd_count = frappe.db.get_value('Food Plan',{'date':date},['sd_head_count'])
                    sd_price = frappe.db.get_value('Food Plan',{'date':date},['sd_price'])  
                    sd_amount = frappe.db.get_value('Food Plan',{'date':date},['sd_amount'])  
                    row13 = [format_date(date),menu.name,sd_count,sd_price,sd_amount]
                    data.append(row13)
            if menu.name == 'Supper Special Food':
                ssf = frappe.db.exists('Food Plan',{'date':date})
                if ssf:
                    ssf_count = frappe.db.get_value('Food Plan',{'date':date},['ssf_head_count'])
                    ssf_price = frappe.db.get_value('Food Plan',{'date':date},['ssf_price'])  
                    ssf_amount = frappe.db.get_value('Food Plan',{'date':date},['ssf_amount'])  
                    row14 = [format_date(date),menu.name,ssf_count,ssf_price,ssf_amount]
                    data.append(row14)
    return data
   

def get_dates(from_date,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates