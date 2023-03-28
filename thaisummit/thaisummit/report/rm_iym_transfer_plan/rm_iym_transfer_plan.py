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
        _('Production Line') + ':Data:120',
        _('Model') + ':Data:120',
        _('location') + ':Data:120',
        _('Responsible Person') + ':Data:120',
        _('Fg Mat') + ':Data:120',
        _('Fg Name') + ':Data:120',
        _('Fg Production Line') + ':Data:120',
        _('Daily Order') + ':Data:120',
        _('Transfer Rate') + ':Data:120',
        _('Packing Std') + ':Data:120',
        _('Prod Req') + ':Data:120',
        _('Final Req') + ':Data:120',
        _('Live Stock') + ':Data:120',
        _('Coverage Day') + ':Data:120',
        _('Req') + ':Data:120',
        _('Transfer Plan') + ':Data:120',
        

    ]
    return column


@frappe.whitelist()
def get_tag_list():
    total_tbs = frappe.db.sql("""select * from `tabTSAI Part Master` where mat_type in ('RM') and customer in ('IYM','HPS')""",as_dict=1)
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
        total_opq = 0
        for do in dos:
            if do['item'] == tbs['name']:
                daily_order = do['daily_order']
                min_qty = do['min_qty']
                max_qty = do['max_qty']
        get_fms = frappe.get_all('TSAI BOM',{'item': tbs['name']},['fm','item_quantity'])
        get_fg_prod_line = frappe.db.get_value('TSAI Part Master',{'mat_no':tbs['fg_mat']},['production_line'])
       
        for fm in get_fms:
            if frappe.get_value('TSAI Part Master',{'mat_no':fm['fm']},'mat_type') == 'FG':
                opq_qty = get_opq(fm['fm'])
                total_opq += flt(fm['item_quantity']) * opq_qty
                # frappe.log_error("total_opq:"+str(total_opq)+"/opq_qty:"+str(opq_qty)+"/fm:"+str(fm['fm'])+"/Qty:"+str(fm['item_quantity']))
        #opq = get_open_production_qty(tbs['name']) or 0
        opq = total_opq
        
        packing_std = tbs['packing_std']
        max_stock = math.ceil(
            (daily_order * tbs['max_day'])/packing_std)*packing_std
        min_stock = math.ceil(
            (daily_order * tbs['min_day'])/packing_std)*packing_std
        live_stock = get_live_stock(tbs['name'])
        if cint(daily_order) > 0 and cint(live_stock) > 0:
            coverage_day = live_stock / daily_order
        else:
            coverage_day = 0
        final_req  =  math.ceil( opq * (tbs['transfer_rate']))
        if (final_req - live_stock) < 0:
            transfer_plan = 0
        else:
            transfer_plan = math.ceil((final_req - live_stock)/packing_std)*packing_std
            # transfer_plan = math.ceil(final_req)*packing_std

        req = 0
        if (final_req - live_stock) < 0:
            req = 0
        else:
            req = math.ceil(final_req - live_stock)
        openqty = 0
        updated_tbs_dict['parts_name'] = (tbs['parts_name'])
        updated_tbs_dict['parts_no'] = tbs['parts_no']
        updated_tbs_dict['transfer_plan'] = round(transfer_plan)
        updated_tbs_dict['daily_order'] = daily_order
        updated_tbs_dict['production_line'] =tbs['production_line']
        updated_tbs_dict['location'] =tbs['rack_no']
        updated_tbs_dict['responsible_person'] =tbs['rack_resposible_person']		
        updated_tbs_dict['model'] = tbs['model']
        updated_tbs_dict['packing_std'] = packing_std
        updated_tbs_dict['prod_req'] = round(opq)
        updated_tbs_dict['customer'] = tbs['customer']
        updated_tbs_dict['transfer_rate'] = tbs['transfer_rate']
        updated_tbs_dict['mat_no'] = tbs['name']
        updated_tbs_dict['final_req'] = round(final_req)
        updated_tbs_dict['live_stock'] = round(live_stock)
        updated_tbs_dict['coverage_day'] = round(coverage_day,1)
        updated_tbs_dict['req'] = req
        updated_tbs_dict['fg_mat'] = tbs['fg_mat']
        updated_tbs_dict['fg_name'] = tbs['fg_name']
        updated_tbs_dict['fg_production_line'] = get_fg_prod_line
        updated_tbs_list.append(updated_tbs_dict.copy())
        count += 1

    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")
    updated_tbs_list = sorted(updated_tbs_list, key=lambda d: d['coverage_day'])
    data = [updated_tbs_list, current_datetime]
    return updated_tbs_list


def get_opq(fm):
    total_open_qty = 0
    if frappe.db.exists('TSAI Part Master',{'mat_no':fm}):
        
        url = "http://172.16.1.18/StockDetail/Service1.svc/GetOpenProductionOrder"
        payload = json.dumps({
            "ProductNo": fm,
            "Fromdate": "",
            "Todate": ""
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request(
            "POST", url, headers=headers, data=payload)
        openqty = 0
        if response:
            stocks = json.loads(response.text)
            if stocks:
                openqty = stocks[0]['OpenQty']
                completed_qty = stocks[0]['CmpltQty']
                planned_qty = stocks[0]['PlannedQty']
                for stock in stocks:
                    total_open_qty += cint(stock['OpenQty'])
    return total_open_qty


def get_parent_open_qty(mat_no):
    total_open_qty = 0
    url = "http://172.16.1.18/StockDetail/Service1.svc/GetOpenProductionOrder"
    payload = json.dumps({
        "ProductNo": mat_no,
        "Fromdate": "",
        "Todate": ""
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request(
        "POST", url, headers=headers, data=payload)
    openqty = 0
    if response:
        stocks = json.loads(response.text)
        if stocks:
            openqty = stocks[0]['OpenQty']
            completed_qty = stocks[0]['CmpltQty']
            planned_qty = stocks[0]['PlannedQty']
            for stock in stocks:
                total_open_qty += cint(stock['OpenQty'])
    return total_open_qty

def get_open_production_qty(mat_no):
    open_qty = 0
    reqd_open_qty = 0
    parent_mat = frappe.db.exists('TSAI BOM',{'item':mat_no,'depth':1})
    if parent_mat:
       open_qty =  get_parent_open_qty(mat_no)
    else:
        fms = frappe.get_all('TSAI BOM',{'item':mat_no,'depth':('!=','1')},['fm','item_quantity'])
        for fm in fms:
            mat_type = frappe.get_value('TSAI Part Master',fm['fm'],'mat_type')
            if mat_type == 'FG':
                reqd_open_qty = get_parent_open_qty(fm['fm'])
                open_qty += flt(reqd_open_qty) * flt(fm['item_quantity'])
    return open_qty
    
   
    

            
def get_live_stock(mat_no):
    
    url = "http://172.16.1.18/StockDetail/Service1.svc/GetItemInventory"
    payload = json.dumps({
        "ItemCode": mat_no,
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request(
        "POST", url, headers=headers, data=payload)
    stock = 0
    if response:
        stocks = json.loads(response.text)
        if stocks:
            ica = frappe.db.sql(
                "select warehouse from `tabInventory Control Area` where rm_transfer_plan = 'Y' ", as_dict=True)

            wh_list = [d['warehouse'] for d in ica if 'warehouse' in d]

            df = pd.DataFrame(stocks)
            df = df[df['Warehouse'].isin(wh_list)]
            stock = pd.to_numeric(df["Qty"]).sum()
        return stock