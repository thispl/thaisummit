# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

from calendar import month
import frappe
# from datetime import date, timedelta
from frappe import msgprint, _
from warnings import  filters
from frappe.utils import cstr, cint, getdate
from frappe.utils import cstr, add_days, date_diff, getdate,today
from datetime import date, timedelta, datetime
import pandas as pd
import math
import requests
import json
from frappe.utils import (
	flt,
	cint,
	cstr,
	get_html_format,
	get_url_to_form,
	gzip_decompress,
	format_duration,
)


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    columns = [
        _('Mat No') + ':Data/:100',
        _('Part No') + ':Data/:150',
        _('Part Name') + ':Data/:200',
        _('Model') + ':Data/:80',
        _('Packing') + ':Data/:80',
        ]
    for i in range(8):
        dt = datetime.strptime(add_days(today(),i),'%Y-%m-%d')
        columns.append(_('%s'%datetime.strftime(dt,'%d-%b')) + ':Data/:80')
    return columns

def get_data(filters):
    data = []
    url = "http://172.16.1.18/StockDetail/Service1.svc/GetPOLineDetails"
    date = datetime.strptime(today(), '%Y-%m-%d')
    date = datetime.strftime(date, "%Y%m%d")
    payload = json.dumps({
        "Fromdate": "",
        "Todate": "",
        "SupplierCode": filters.supplier_code,
        "DeliveryDate": date,
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        pos = json.loads(response.text)
    except:
        frappe.msgprint("Unable to display Pickup Plan due to API Issue")

    x = 1
    if pos:
        for po in pos:
            if po['Po_Status'] == 'O':
                if frappe.db.exists('TSAI Part Master',po['Mat_No']):
                    pr_name = frappe.db.get_value('Prepared Report',{'report_name':'Supplier Daily Order','status':'Completed'},'name')
                    attached_file_name = frappe.db.get_value(
                        "File",
                        {"attached_to_doctype": 'Prepared Report', "attached_to_name": pr_name},
                        "name",
                    )
                    attached_file = frappe.get_doc("File", attached_file_name)
                    compressed_content = attached_file.get_content()
                    uncompressed_content = gzip_decompress(compressed_content)
                    dos = json.loads(uncompressed_content.decode("utf-8"))

                    max_qty = 0
                    for do in dos:
                        if do['item'] == po['Mat_No']:
                            max_qty = do['max_qty']

                    open_qty = float(po['Open_Qty'])
                    in_transit_qty = 0

                    url = "http://172.16.1.18/StockDetail/Service1.svc/GetItemInventory"
                    payload = json.dumps({
                    "ItemCode": po['Mat_No']
                    })
                    headers = {
                    'Content-Type': 'application/json'
                    }
                    response = requests.request("POST", url, headers=headers, data=payload)
                    stock = 0
                    if response:
                        stocks = json.loads(response.text)
                        if stocks:
                            ica = frappe.db.sql("select warehouse from `tabInventory Control Area` where invoice_key = 'Y' ",as_dict=True)

                            wh_list = [d['warehouse'] for d in ica if 'warehouse' in d]

                            df = pd.DataFrame(stocks)
                            df = df[df['Warehouse'].isin(wh_list)]
                            stock = pd.to_numeric(df["Qty"]).sum()

                    t_qty = stock+in_transit_qty
                    req_qty = '-'
                    packing_std = frappe.db.get_value(
                        "TSAI Part Master", po['Mat_No'], 'packing_std')
                    model = frappe.db.get_value(
                        "TSAI Part Master", po['Mat_No'], 'model')
                    share = frappe.db.get_value('Shares of Business Entry',{'supplier_code':filters.supplier_code,'mat_no':po['Mat_No']},'share_of_business') or '-'
                    if open_qty > 0:
                        if t_qty < max_qty:
                            if share != '-' :
                                req_qty = ((math.floor(
                                (max_qty - t_qty)/packing_std)*packing_std)*share)/100
                            else:
                                req_qty = math.floor(
                                (max_qty - t_qty)/packing_std)*packing_std
                            if req_qty == 0:
                                req_qty = '-'
                    row = [po['Mat_No'],po['Part_No'],po['Part_Name'],model,packing_std,req_qty]
                    x += 1
                    for do in dos:
                        if do['item'] == po['Mat_No']:
                            tomorrow = add_days(today(),1)
                            for i in range(7):
                                dt = datetime.strptime(add_days(tomorrow,i),'%Y-%m-%d')
                                day = datetime.strftime(dt,'%d')
                                month = datetime.strftime(dt,'%b')
                                qty = do[day+'_'+month.lower()]
                                if qty == 0:
                                    qty = '-'
                                row.append(qty)
                    data.append(row)
    return data