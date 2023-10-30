# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import math
import frappe
import json
import requests
import pandas as pd
import openpyxl
from six import BytesIO
from frappe.utils import (
    flt,
    cint,
    cstr,
    get_html_format,
    get_url_to_form,
    gzip_decompress,
    format_duration,
    today
)
from datetime import timedelta, datetime
# from __future__ import unicode_literals
from six.moves import range
from six import string_types
import frappe
import json
from frappe.utils import getdate, cint, add_months, date_diff, add_days, nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate
import pandas as pd 
# from __future__ import unicode_literals
from functools import total_ordering
from itertools import count,groupby
# import more_itertools
import frappe
from frappe import permissions
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
from math import floor
from frappe import msgprint, _
from calendar import month, monthrange
from datetime import date, timedelta, datetime,time
from numpy import true_divide 
from operator import itemgetter





def execute(filters=None):
    columns, data = [] ,[]
    columns = get_columns()
    data = get_tag_list()
    return columns, data

def get_columns():
    column = [
        _('Mat No') + ':Data:120',
        _('Parts No') + ':Data:120',
        _('Parts Name') + ':Data:120',
        _('Mat Type') + ':Data:120',
        _('Customer') + ':Data:120',
        _('Model') + ':Data:120',
        
        _('Production Line') + ':Data:120',
        _('Manpower Std') + ':Data:120',
        _('Cycle Time') + ':Data:120',
        _('Uph') + ':Data:120',
        _('Unit Per Shift') + ':Data:120',
        _('Cap') + ':Data:120',
        _('Packing Std') + ':Data:120',
        _('Daily Order') + ':Data:120',
        _('Max Day') + ':Data:120',
        _('Max Qty') + ':Data:120',
        _('Min Day') + ':Data:120',
        _('Min Qty') + ':Data:120',
        _('Live Stock') + ':Data:120',
        _('Coverage') + ':Float:120',
        
        _('Require Qty') + ':Data:120',
        _('Require Headcount') + ':Float:120',
        _('Required Hr') + ':Float:120',
        _('Pending Qty') + ':Data:120',
        _('Pending Headcount') + ':Data:120',
        _('Pending Hr') + ':Float:120',
        _('Today Qty') + ':Data:120',
        _('Today Headcount') + ':Data:120',
        _('Today Hr') + ':Float:120',
        _('Today Qty After Adj') + ':Data:120',
        _('Today Headcount After Adj') + ':Data:120',
        _('Today Hr After Adj') + ':Data:120',
        _('Total Qty') + ':Data:120',
        _('total headcount') + ':Data:120',
        _('Total Hr') + ':Float:120',
        _('Check') + ':Data:120',

        
    
    ]
    return column


@frappe.whitelist()
def get_tag_list():
    total_tbs = frappe.db.sql("""select * from `tabTSAI Part Master` where customer in ('IYM','HPS')""",as_dict=1)
    
    updated_tbs_list = []
    updated_tbs_dict = {}
    pr_name = frappe.db.get_value(
        'Prepared Report', {'report_name': 'Production Daily Order', 'status': 'Completed'}, 'name')

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

    daily_order = 0
    min_qty = 0
    max_qty = 0
    count = 0
    
    for tbs in total_tbs:
        packing_std = cint(tbs['packing_std'])
        pending_qty = get_opq(tbs['mat_no'])
        min_day = tbs['min_day']
        max_day = tbs['max_day']
        for do in dos:
            if do['item'] == tbs['mat_no']:
                daily_order = do['daily_order']
                live_stock = get_live_stock(tbs['mat_no'])
        adjustable_percentage = frappe.get_single('Ekanban Settings').adjustable_percent
        percent = 0.8
        coverage_day = max_qty - daily_order
        min_qty = math.ceil((daily_order * min_day)/packing_std)*packing_std
        max_qty = math.ceil((daily_order * max_day)/packing_std)*packing_std
        
        
        require_qty = 0
        
        if live_stock > min_qty:
            require_qty = 0
        else:
            require_qty = math.ceil((max_qty - live_stock)/packing_std)*packing_std

        require_headcount = 0
        pending_headcount = 0
        required_hr = 0
        pending_hr = 0
        today_qty = 0 
        today_qty1 = 0 
        today_qty2 = 0
        cap = 0
        today_headcount = 0
        today_headcount1 = 0
        today_headcount2 = 0
        today_hr = 0
        today_hr1 = 0
        today_hr2 = 0
        total_hr = 0
        total_headcount2 = 0
        coverage = 0
        if daily_order > 0:
            coverage = round((live_stock / daily_order),1)
        else:
            coverage = "No Plan"
        
        if require_qty - pending_qty > 0:
            today_qty =  require_qty - pending_qty  
        else:
            today_qty = 0
        
        if tbs['uph'] == 0:
            required_hr = 0
            cap = "No Limit"
        elif tbs['uph'] > 0:
            ca = ((tbs['uph'] * 21.75) / packing_std) * packing_std
            cap = round(ca)
            
          
        if daily_order <= 0:
            tdy_qty1 = 0
        elif cap != "No Limit":
            if(today_qty + pending_qty) > cap:
               tdy_qty1 = round(cap / packing_std ) * packing_std
            else:
                tdy_qty1 = today_qty
        elif cap == 'No Limit':
            tdy_qty1 = round(today_qty / packing_std ) * packing_std
       
        # today_qty1 = round((tdy_qty1 * percent) / packing_std) * packing_std
        today_qty1 = round(tdy_qty1)
        
        
        # today_qty1 = math.floor((today_qty * adjustable_percentage) / packing_std) * packing_std
        
        
        if tbs['uph'] > 0:
            if require_qty > 0:
                require_headcount = round((require_qty / (tbs['uph'] * 8)) * tbs['manpower_std'],2)
                required_hr = round((require_qty / (tbs['uph'])),2)
            if pending_qty > 0:
                pending_headcount = round((pending_qty / (tbs['uph'] * 8)) * tbs['manpower_std'],2)
                pending_hr = round((pending_qty / tbs['uph']),2)
            if today_qty > 0:
                total_hr = round((today_qty / tbs['uph']),2)
                today_headcount = round((today_qty / (tbs['uph'] * 8)) * tbs['manpower_std'],2)
                today_hr = round((today_qty / tbs['uph']),2)
            if today_qty1 > 0:
                today_headcount1 = round((today_qty1 / (tbs['uph'] * 8)) * tbs['manpower_std'],2)
            if today_headcount1 > 0:
                today_hr1 = round((today_headcount1 / tbs['uph']),2)
   
        
        if cap != 'No Limit':
            if total_hr > cap :
                check = 'Over Cap'
            else:
                check = "-"
        
        
        total_qty = today_qty1 + pending_qty
        if tbs['uph'] > 0 :
            total_headcount = round((total_qty / (tbs['uph'] * 8)) * tbs['manpower_std'],2)
            total_hr = round((total_qty / tbs['uph']),2)
       
            
        
    
        if frappe.db.exists("TSAI BOM",{"item":tbs.name,"bom_type":"production"}):
            updated_tbs_dict['mat_no'] = tbs['mat_no']
            updated_tbs_dict['parts_name'] = (tbs['parts_name'])
            updated_tbs_dict['parts_no'] = tbs['parts_no']
            updated_tbs_dict['mat_type'] = (tbs['mat_type'])
            updated_tbs_dict['model'] = tbs['model']
            updated_tbs_dict['production_line'] = tbs['production_line'] 
            updated_tbs_dict['customer'] = tbs['customer']
            updated_tbs_dict['manpower_std'] = tbs['manpower_std']
            updated_tbs_dict['cycle_time'] = tbs['cycle_time']
            updated_tbs_dict['uph'] = tbs['uph']
            updated_tbs_dict['unit_per_shift'] = tbs['uph'] * 8
            updated_tbs_dict['packing_std'] = packing_std
            updated_tbs_dict['daily_order'] = daily_order
            updated_tbs_dict['max_day'] = tbs['max_day']
            updated_tbs_dict['max_qty'] = round(max_qty)
            updated_tbs_dict['min_day'] = tbs['min_day']
            updated_tbs_dict['min_qty'] = round(min_qty)
            updated_tbs_dict['live_stock'] = get_live_stock(tbs['mat_no'])
            updated_tbs_dict['coverage'] = coverage
            updated_tbs_dict['pending_qty'] = pending_qty
            updated_tbs_dict['require_qty'] = require_qty
            updated_tbs_dict['require_headcount'] = require_headcount
            updated_tbs_dict['required_hr'] = required_hr
            updated_tbs_dict['cap'] = cap
            updated_tbs_dict['pending_headcount'] = pending_headcount
            updated_tbs_dict['pending_hr'] = pending_hr
            updated_tbs_dict['today_qty'] = round(today_qty)
            updated_tbs_dict['today_headcount'] = today_headcount
            updated_tbs_dict['today_hr'] = today_hr
            updated_tbs_dict['today_qty_after_adj'] = round(today_qty1)
            updated_tbs_dict['today_headcount_after_adj'] = today_headcount1
            updated_tbs_dict['today_hr_after_adj'] = today_hr1
            updated_tbs_dict['total_qty'] = total_qty
            updated_tbs_dict['total_headcount'] = total_headcount
            updated_tbs_dict['total_hr'] = total_hr
            updated_tbs_dict['check'] = check
            updated_tbs_dict['coverage_day'] = round(coverage_day,1)
            updated_tbs_list.append(updated_tbs_dict.copy())
            count += 1
    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")
    updated_tbs_list = sorted(updated_tbs_list, key=lambda d: d['coverage_day'])
   
    data = [updated_tbs_list]
   
    
    return updated_tbs_list



def get_live_stock(mat_no):
    
    url = "http://apioso.thaisummit.co.th:10401/api/GetItemInventory"
    payload = json.dumps({
        "ItemCode": mat_no,
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
                "select warehouse from `tabInventory Control Area` where iym = 'Y' ", as_dict=True)

            wh_list = [d['warehouse'] for d in ica if 'warehouse' in d]

            df = pd.DataFrame(stocks)
            df = df[df['Warehouse'].isin(wh_list)]
            stock = pd.to_numeric(df["Qty"]).sum()
        return stock or 0

def get_opq(fm):
    total_open_qty = 0
    if frappe.db.exists('TSAI Part Master',{'mat_no':fm}):
        if frappe.get_value('TSAI Part Master',{'mat_no':fm},['mat_type']) in ['FG','INH','BOP']:
            url = "http://apioso.thaisummit.co.th:10401/api/OpenProductionOrder"
            payload = json.dumps({
                "ProductNo": fm,
                "Fromdate": "",
                "Todate": ""
            })
            headers = {
                'Content-Type': 'application/json',
                'API_KEY': '/1^i[#fhSSDnC8mHNTbg;h^uR7uZe#ninearin!g9D:pos+&terpTpdaJ$|7/QYups;==~w~!AWwb&DU'
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload)
            openqty = 0
            if response:
                stocks = json.loads(response.text)
                if stocks:
                    openqty = stocks[0]['OpenQty']
                    completed_qty = stocks[0]['CmpltQty']
                    # planned_qty = stocks[0]['PlannedQty']
                    for stock in stocks:
                        total_open_qty += cint(stock['OpenQty'])
    return total_open_qty