# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
# from datetime import date, timedelta
from frappe import msgprint, _
from warnings import  filters
from frappe.utils import cstr, cint, getdate
from frappe.utils import cstr, add_days, date_diff, getdate,today,gzip_decompress
from datetime import date, timedelta, datetime
import pandas as pd
import json

def execute(filters=None):
    # from_date = '2021-11-01'
    # from_date = today()
    # to_date = today()
    from_date = today()
    to_date = add_days(from_date,7)
    dates = get_dates(from_date,to_date)
    holiday = check_holiday(from_date,to_date)
    # to_date = add_days(from_date,6 + len(holiday))
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

    pr_name = frappe.db.get_value(
                    'Prepared Report', {'report_name': 'Supplier Daily Order Test','status':'Completed'}, 'name')
    attached_file_name = frappe.db.get_value(
        "File",
        {"attached_to_doctype": 'Prepared Report',
            "attached_to_name": pr_name},
        "name",
    )
    attached_file = frappe.get_doc("File", attached_file_name)
    compressed_content = attached_file.get_content()
    uncompressed_content = gzip_decompress(compressed_content)
    dos = json.loads(uncompressed_content.decode("utf-8"))
    
    for do in dos:
        row = [do['item'],do['part_no'],do['part_name'],do['cus'],do['model'],do['prod_line'],do['packing']]
        day = 0
        for date in dates:
            date = datetime.strptime(str(date),'%Y-%m-%d')
            d = date.strftime('%d')
            m = date.strftime('%b')
            date_formatted = d + '_' + m.lower()
            forecast_qty = do[date_formatted]
            row.append(do[date_formatted])
            if forecast_qty > 0:
                day += 1
        total_qty = do['total']
        if day > 0:
            daily_order = round(total_qty / day)
        else:
            daily_order = 0
        master = frappe.get_doc('TSAI Part Master',do['item'])
        min_qty = round(daily_order * round(master.min_day,1))
        max_qty = round(daily_order * round(master.max_day,1))
        row.extend([total_qty,day,daily_order,round(master.min_day,1),min_qty,round(master.max_day,1),max_qty])
        data.append(row)
    return data

    # cols = ['Item', 'Part No', 'Part Name', 'Cus', 'Model', 'PROD Line', 'Packing',]
    # for date in dates:
    #     date = datetime.strptime(str(date),'%Y-%m-%d')
    #     d = date.strftime('%d')
    #     m = date.strftime('%b')
    #     cols.append(d + '-' + m)

    # cols += ['Total','Day','Daily Order','Min Day','Min Qty','Max Day','Max Qty']

    
    
    # df = pd.DataFrame(data, columns = cols)
    # df2 = df.groupby(['Item','Part No', 'Part Name', 'Cus', 'Model', 'PROD Line', 'Packing']).sum().reset_index()
    # data_list = df2.values.tolist()
    
    # return data_list

def get_reqd_qty_dates(mat_no):
    day_count = 0
    from_date = add_days(today(),1)
    to_date = add_days(today(),1)
    # from_date = today()
    # to_date = add_days(from_date,6)
    # dates = get_dates(from_date,to_date)
    # holiday = check_holiday(from_date,to_date)
    # to_date = add_days(from_date,6 + len(holiday))
    dates = get_dates(from_date,to_date)

    for day in dates:
        qty1 = frappe.db.sql("""select qty from `tabForecast Data` where mat_no='%s' and date='%s'""" % (mat_no,day),as_dict=True)
        qty = frappe.get_value('Forecast Data',{'mat_no':mat_no,'date':day},'qty') or 0
        if qty > 0:
            day_count += 1
    return day_count

def get_dates(from_date,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates

def check_holiday(from_date,to_date):
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = 'Holiday List - 2021' and holiday_date between '%s' and '%s' """%(from_date,to_date),as_dict=True)
    return holiday