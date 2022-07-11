# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
# from datetime import date, timedelta
from frappe import msgprint, _
from warnings import  filters
from frappe.utils import cstr, cint, getdate
from frappe.utils import cstr, add_days, date_diff, getdate,today
from datetime import date, timedelta, datetime
import pandas as pd


def execute(filters=None):
    # from_date = '2021-11-01'
    from_date = today()
    to_date = add_days(from_date,6)
    dates = get_dates(from_date,to_date)
    holiday = check_holiday(from_date,to_date)
    to_date = add_days(from_date,6 + len(holiday))
    dates = get_dates(from_date,to_date)
    columns = get_columns(dates)
    data = get_data(dates)
    return columns, data

def get_columns(dates):
    columns = [
        _('Item') + ':Data/:150',
        _('Part No') + ':Data/:150',
        _('Part Name') + ':Data/:150',
        _('Cus') + ':Data/:150',
        _('Model') + ':Data/:150',
        _('PROD Line') + ':Data/:150',
        _('Packing') + ':Data/:150',
        ]
    
    for date in dates:
        date = datetime.strptime(str(date),'%Y-%m-%d')
        d = date.strftime('%d')
        m = date.strftime('%b')
        columns.append(d + '-' + m)
    
    columns +=[
        _('Total') + ':Data/:150',
        _('Day') + ':Data/:50',
        _('Daily Order') + ':Data/:150',
        _('Min Day') + ':Data/:150',
        _('Min Qty') + ':Data/:150',
        _('Max Day') + ':Data/:150',
        _('Max Qty') + ':Data/:150',
        ]
    return columns

def get_data(dates):
    data = []
    bom_mats = frappe.get_all('TSAI BOM',{'depth':1},'item',order_by='item')
    for item in bom_mats:
        boms = frappe.get_all('TSAI BOM',{'fm':item.item,'item':('not in',('DL','OHS','DL-HPS','DL-RE','DL-TSSI','OHs-HPS','OHs-RE','OHs-TSSI'))},['item','item_quantity'],order_by='item')
        for bom in boms:
            if frappe.db.exists('TSAI Part Master',bom.item):
                master = frappe.get_doc('TSAI Part Master',bom.item)
                row = [master.mat_no,master.parts_no,master.parts_name,master.customer,master.model,master.production_line,master.packing_std]
                total_qty = 0
                day = 0
                for date in dates:
                    forecast_qty = frappe.db.get_value('Forecast Data',{'mat_no':item.item,'date':date},'qty') or 0
                    total_qty += forecast_qty * bom.item_quantity
                    if forecast_qty > 0:
                        day += 1
                    row.append(forecast_qty*bom.item_quantity)
                if day > 0:
                    daily_order = round(total_qty / day)
                else:
                    daily_order = 0
                min_qty = round(daily_order * round(master.min_day,1))
                max_qty = round(daily_order * round(master.max_day,1))
                row.extend([total_qty,day,daily_order,round(master.min_day,1),min_qty,round(master.max_day,1),max_qty])
                data.append(row)

    forecast_items = frappe.db.sql("select distinct `tabForecast Data`.mat_no as item from `tabForecast Data` where not exists(select `tabTSAI BOM`.item from `tabTSAI BOM` where `tabForecast Data`.mat_no = `tabTSAI BOM`.item) ",as_dict=True)
    for forecast in forecast_items:
        if frappe.db.exists('TSAI Part Master',forecast.item):
            master = frappe.get_doc('TSAI Part Master',forecast.item)
            row = [master.mat_no,master.parts_no,master.parts_name,master.customer,master.model,master.production_line,master.packing_std]
            total_qty = 0
            day = 0
            for date in dates:
                forecast_qty = frappe.db.get_value('Forecast Data',{'mat_no':forecast.item,'date':date},'qty') or 0
                total_qty += forecast_qty
                if forecast_qty > 0:
                    day += 1
                row.append(forecast_qty)
            if day > 0:
                daily_order = round(total_qty / day)
            else:
                daily_order = 0
            min_qty = round(daily_order * round(master.min_day,1))
            max_qty = round(daily_order * round(master.max_day,1))
            row.extend([total_qty,day,daily_order,round(master.min_day,1),min_qty,round(master.max_day,1),max_qty])
            data.append(row)
        
    parts = frappe.get_all('TSAI Part Master',{'direct_part':1},['*'])
    for part in parts:
        row = [part.mat_no,part.parts_no,part.parts_name,part.customer,part.model,part.production_line,part.packing_std]
        total_qty = 0
        day = 0
        for date in dates:
            forecast_qty = frappe.db.get_value('Forecast Data',{'mat_no':part.name,'date':date},'qty') or 0
            total_qty += forecast_qty
            if forecast_qty > 0:
                day += 1
            row.append(forecast_qty)
        if day > 0:
            daily_order = round(total_qty / day)
        else:
            daily_order = 0
        min_qty = round(daily_order * round(part.min_day,1))
        max_qty = round(daily_order * round(part.max_day,1))
        row.extend([total_qty,day,daily_order,round(part.min_day,1),min_qty,round(part.max_day,1),max_qty])
        data.append(row)

    cols = ['Item', 'Part No', 'Part Name', 'Cus', 'Model', 'PROD Line', 'Packing',]

    for date in dates:
        date = datetime.strptime(str(date),'%Y-%m-%d')
        d = date.strftime('%d')
        m = date.strftime('%b')
        cols.append(d + '-' + m)

    cols += ['Total','Day','Daily Order','Min Day','Min Qty','Max Day','Max Qty']

    df = pd.DataFrame(data, columns = cols)
    df2 = df.groupby(['Item','Part No', 'Part Name', 'Cus', 'Model', 'PROD Line', 'Packing']).sum().reset_index()
    data_list = df2.values.tolist()
    return data_list

def get_dates(from_date,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates

def check_holiday(from_date,to_date):
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = 'Holiday List - 2021' and holiday_date between '%s' and '%s' """%(from_date,to_date),as_dict=True)
    return holiday