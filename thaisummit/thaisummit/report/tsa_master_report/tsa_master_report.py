# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import add_days, data
from datetime import datetime,date
from frappe.utils import cstr, add_days, date_diff,format_datetime,format_date
from frappe.utils import today


def execute(filters=None):
    columns = get_columns(filters=None)
    data = get_data(filters=None)
    return columns, data


def get_columns(filters=None):
    columns = []
    columns+= [
        _("IYM Model code") + ":Data:120",
        _("WELD/ACED/ASSY/FUELTANK") + ":Data:200",
        _("TSAI MODEL CODE") + ":Data:200",
        _("MAT NO") + ":Data:100",
        _("PART NO") + ":Data:200",
        _("PART NAME") + ":Data:200",
        _("USAGE") + ":Data:100",
    ]
    from_date = today()
    to_date = add_days(from_date,2)
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    
    for date in dates:
        d = datetime.strptime(date,'%Y-%m-%d')
        date = d.strftime('%d-%b')
        columns+=[
            _(date) +":Data:100",
        ]
    
    d1 = datetime.strptime(add_days(to_date,1),'%Y-%m-%d')
    d1 = d1.strftime('%d-%b')
    d2 = datetime.strptime(add_days(to_date,2),'%Y-%m-%d')
    d2 = d2.strftime('%d-%b')
    columns+=[
        _("SUM") + ":Data:80",
        _("DAY") + ":Data:80",
        _("DAILY ORDER") + ":Data:120",
        _(d1) + ":Data:80",
        _(d2) + ":Data:80",
    ]

    return columns

def get_data(filters=None):
    data = []
    from_date = today()
    to_date = add_days(from_date,2)
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    master = frappe.db.sql("""select DISTINCT mat_no, part_no,part_name,iym_model_code,section,tsai_model_code from `tabTSA Master` where date between '%s' and '%s' """%(from_date,to_date),as_dict=True)
    for m in master:
        daily_order = frappe.db.sql("""select sum(quantity) as total from `tabTSA Master` where mat_no = '%s' and date between '%s' and '%s' """%(m.mat_no,from_date,to_date),as_dict=True)
        usage = frappe.db.get_value('Part Master',m.part_no,'usage')
        row = [m.iym_model_code,m.section,m.tsai_model_code,m.mat_no,m.part_no,m.part_name,usage]
        days = 0
        sum = 0
        for date in dates:
            qty = frappe.db.get_value('TSA Master',{'mat_no':m.mat_no,'date':date},'quantity') or '-'
            if qty != '-':
                days += 1
                sum += int(qty)
            row.append(qty)
        try:
            daily_order = round(daily_order[0].total/days)
        except:
            daily_order = '-'
        row.extend([sum,days,daily_order])
        upcoming_qty1 = frappe.db.get_value('TSA Master',{'mat_no':m.mat_no,'date':add_days(to_date,1)},'quantity') or '-'
        upcoming_qty2 = frappe.db.get_value('TSA Master',{'mat_no':m.mat_no,'date':add_days(to_date,2)},'quantity') or '-'
        row.extend([upcoming_qty1,upcoming_qty2])
        data.append(row)
        # data.extend(qty_list)
    # itemgroup = []
    # itemgroup = frappe.db.sql("""SELECT sum(quantity) as quantity,part_no FROM `tabTSA Master` where date = '2021-07-21' group by iym_model_code """ ,as_dict=True)
    # frappe.errprint(itemgroup)

    # for d in item_group:
        
    #     usage = frappe.get_value("Part Master",{'name':d.part_no},['usage','name'])
    #     u = usage[0]
    #     date1 = datetime.strftime(d.date,"%Y-%m-%d")
    #     quantity = 0

    #     if date1 == date[0]:
    #         quantity = frappe.db.sql("""SELECT sum(quantity) as q from `tabTSA Master` WHERE iym_model_code='B7JK00'
    #         AND section='ACED' AND part_no='B7JK00-B7JF7111000080-ACED' """,as_dict=True)
    #         frappe.errprint(quantity)

        # elif date1 == date[1]:
        #     quantity = 0
        #     quantity+= int(frappe.get_value("TSA Master",{'iym_model_code':"B7JK00",'section':'ACED','part_no':'B7JK00-B7JF7111000080-ACED'},['quantity']))
                
        #     frappe.errprint("hi--------2")
        #     frappe.errprint(quantity)

        # elif date1 == date[2]:
        #     quantity = 0
        #     quantity+= int(frappe.get_value("TSA Master",{'iym_model_code':"B7JK00",'section':'ACED','part_no':'B7JK00-B7JF7111000080-ACED'},['quantity']))
        #     frappe.errprint("hi-----------3")
        #     frappe.errprint(quantity)

        # data.append([d.iym_model_code,d.section,'a',d.mat_no,d.part_no,d.part_name,usage[0],quantity,quantity,quantity,"e","f","g"])

    return data

