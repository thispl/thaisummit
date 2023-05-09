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

no_cache = 1


def get_context(context):
    if frappe.session.user != 'Guest':
        context.tag_list = get_tag_list()


@frappe.whitelist()
def get_tag_list():
    total_tbs = frappe.db.sql("""select * from `tabTSAI Part Master` where mat_no like '10%' and mat_type = 'FG' """,as_dict=1)
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
    for tbs in total_tbs[:300]:
        for do in dos:
            if do['item'] == tbs['mat_no']:
                daily_order = do['daily_order']
                min_qty = do['min_qty']
                max_qty = do['max_qty']
        if daily_order > 0:
            packing_std = tbs['packing_std']
            max_stock = math.ceil(
                (daily_order * tbs['max_day'])/packing_std)*packing_std
            min_stock = math.ceil(
                (daily_order * tbs['min_day'])/packing_std)*packing_std
            live_stock = get_live_stock(tbs['mat_no'])
            coverage_day = live_stock / daily_order
            req = 0
            if live_stock >= min_stock:
                req = 0
            if live_stock < min_stock:
                req = math.ceil((max_stock - live_stock) / packing_std)*packing_std
            openqty = 0
            updated_tbs_dict['parts_name'] = tbs['parts_name']
            updated_tbs_dict['parts_no'] = tbs['parts_no']
            updated_tbs_dict['model'] = tbs['model']
            updated_tbs_dict['packing_std'] = packing_std
            updated_tbs_dict['daily_order'] = daily_order
            updated_tbs_dict['customer'] = tbs['customer']
            updated_tbs_dict['production_line'] = tbs['production_line']
            updated_tbs_dict['mat_no'] = tbs['mat_no']
            updated_tbs_dict['min_day'] = tbs['min_day']
            updated_tbs_dict['min_stock'] = min_stock
            updated_tbs_dict['max_day'] = tbs['max_day']
            updated_tbs_dict['max_stock'] = max_stock
            updated_tbs_dict['live_stock'] = round(live_stock)
            updated_tbs_dict['coverage_day'] = round(coverage_day,1)
            updated_tbs_dict['req'] = req
            updated_tbs_dict['openqty'] = get_open_production_qty(tbs['mat_no'])
            updated_tbs_list.append(updated_tbs_dict.copy())
            count += 1

    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")
    updated_tbs_list = sorted(updated_tbs_list, key=lambda d: d['coverage_day'])
    data = [updated_tbs_list, current_datetime]
    return data

@frappe.whitelist()
def get_tag_list_xlsx():
    # total_tbs = frappe.get_all('TSAI Part Master', {'customer': (
    #     'in', ['HPS', 'IYM'])}, ['*'], order_by="mat_no")
    total_tbs = frappe.db.sql("""select * from `tabTSAI Part Master` where mat_no like '10%' and mat_type = 'FG' """,as_dict=1)
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
        for do in dos:
            if do['item'] == tbs['mat_no']:
                daily_order = do['daily_order']
                min_qty = do['min_qty']
                max_qty = do['max_qty']
        if daily_order > 0:
            packing_std = tbs['packing_std']
            max_stock = math.ceil(
                (daily_order * tbs['max_day'])/packing_std)*packing_std
            min_stock = math.ceil(
                (daily_order * tbs['min_day'])/packing_std)*packing_std
            live_stock = get_live_stock(tbs['mat_no'])
            coverage_day = live_stock / daily_order
            req = 0
            if live_stock >= min_stock:
                req = 0
            if live_stock < min_stock:
                req = math.ceil((max_stock - live_stock) / packing_std)*packing_std
            openqty = 0
            updated_tbs_dict['parts_name'] = tbs['parts_name']
            updated_tbs_dict['parts_no'] = tbs['parts_no']
            updated_tbs_dict['model'] = tbs['model']
            updated_tbs_dict['packing_std'] = packing_std
            updated_tbs_dict['daily_order'] = daily_order
            updated_tbs_dict['customer'] = tbs['customer']
            updated_tbs_dict['production_line'] = tbs['production_line']
            updated_tbs_dict['mat_no'] = tbs['mat_no']
            updated_tbs_dict['min_day'] = tbs['min_day']
            updated_tbs_dict['min_stock'] = min_stock
            updated_tbs_dict['max_day'] = tbs['max_day']
            updated_tbs_dict['max_stock'] = max_stock
            updated_tbs_dict['live_stock'] = round(live_stock)
            updated_tbs_dict['coverage_day'] = round(coverage_day,1)
            updated_tbs_dict['req'] = req
            updated_tbs_dict['openqty'] = get_open_production_qty(tbs['mat_no'])
            updated_tbs_list.append(updated_tbs_dict.copy())
            count += 1

    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")
    updated_tbs_list = sorted(updated_tbs_list, key=lambda d: d['coverage_day'])
    data = [updated_tbs_list, current_datetime]
    return data

def get_live_stock(mat_no):
    qty = 0
    from datetime import date
    today = date.today()
    stock1 = frappe.get_value('Live Stock Quantity',{'live_stock_date':today,'mat_no':mat_no},['stock'])
    if stock1:
        qty = flt(stock1)
    return qty
    
# def get_live_stock(mat_no):
#     url = "http://apioso.thaisummit.co.th:10401/api/GetItemInventory"
#     payload = json.dumps({
#         "ItemCode": mat_no
#     })
#     headers = {
#         'Content-Type': 'application/json'
#     }
#     response = requests.request(
#         "POST", url, headers=headers, data=payload)
#     stock = 0
#     if response:
#         stocks = json.loads(response.text)
#         if stocks:
#             ica = frappe.db.sql(
#                 "select warehouse from `tabInventory Control Area` where invoice_key = 'Y' ", as_dict=True)

#             wh_list = [d['warehouse'] for d in ica if 'warehouse' in d]

#             df = pd.DataFrame(stocks)
#             df = df[df['Warehouse'].isin(wh_list)]
#             stock = pd.to_numeric(df["Qty"]).sum()
#     return stock

def get_open_production_qty(mat_no):
    qty = 0
    from datetime import date
    today = date.today()
    openqty = frappe.get_value('Open Production Order',{'daily_order_date':today,'mat_no':mat_no},['open_qty'])
    if openqty:
        qty = flt(openqty)
    return qty

@frappe.whitelist()
def download_excel():
    data = []
    updated_tbs_list = get_tag_list_xlsx()
    for d in updated_tbs_list[0]:
        data.append([
            d['customer'],
            d['mat_no'],
            d['parts_no'],
            d['parts_name'],
            d['production_line'],
            d['model'],
            d['packing_std'],
            d['daily_order'],
            d['max_day'],
            d['max_stock'],
            d['min_day'],
            d['min_stock'],
            d['live_stock'],
            d['coverage_day'],
            d['req'],
            d['openqty']
        ])
    xlsx_file = make_xlsx(data)
    frappe.response['filename'] = 'FG_IYM_Live.xlsx'
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type'] = 'binary'


def make_xlsx(data, sheet_name=None, wb=None, column_widths=None):
    # args = frappe.local.form_dict
    column_widths = column_widths or []
    if wb is None:
        wb = openpyxl.Workbook()

    ws = wb.create_sheet(sheet_name, 0)

    cols = ["Customer", "Mat No", "Parts no", "Parts Name", "Line", "Model", "Packing Std.", "Daily Order",
            "Max Day", "Max Stock", "Min Day", "Min Stock", "Stock", "Coverage Days", "Req", "Production Plan"]
    ws.append(cols)

    for row in data:
        ws.append(row)

    ws.sheet_view.zoomScale = 80

    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    return xlsx_file


@frappe.whitelist()
def chop_microseconds(delta):
    return delta - datetime.timedelta(microseconds=delta.microseconds)
