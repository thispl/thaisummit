# Copyright (c) 2023, TEAMPRO and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.model.document import Document
import frappe
from frappe.model.document import Document
import math
import frappe
import json
import requests
import pandas as pd
import openpyxl
from frappe import _
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
from frappe.utils import getdate,get_time, cint, add_months, date_diff, add_days, nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime
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
from frappe.utils import cstr, add_days, date_diff, getdate, format_date,now
from math import floor
from frappe import msgprint, _
from calendar import month, monthrange
from datetime import date, timedelta, datetime,time
from numpy import true_divide 
from operator import itemgetter

class TagCardGeneration(Document):
	def validate(self):
		if self.production_order_qty == 0:
			frappe.throw(_('Production Order Qty is Zero'))

		self.shift = get_shift_type()
		self.date = date.today()
		u_name = frappe.db.sql("""select username from `tabUser` where name='%s' """%(frappe.session.user),as_dict=1)[0]
		self.user_name = u_name['username']
		self.set('table_9', [])
		q_ty = float(self.quantity)
		pack_std = float(self.packing_std)
		qty_clac =  q_ty / pack_std
		q_clac = int(qty_clac)
		qr_list = []
		for i in range(q_clac):
			new_string = "{}-{}".format(self.name, i)			
			self.append('table_9',{
				'item_card_no':new_string,
				'mat_no':self.mat_number,
				'packing_standard':self.packing_std,
				'production_order':self.production_order_qty,
				'qty':self.packing_std
				
			})
			qr_list.append(new_string)
		my_string = ','.join(qr_list)
		self.qr_code = my_string
		table = self.table_9
		for t in table:
			tab = frappe.new_doc("Tag Card")
			tab.item_card_no = t.item_card_no
			tab.production_order_qty = t.production_order
			tab.mat_number = self.mat_number
			tab.mat_name = self.mat_name
			tab.part_number = self.part_number
			tab.packing_std = t.packing_standard
			tab.quantity = t.qty
			tab.link_document = self.name
			tab.save(ignore_permissions=True)
			frappe.db.commit()
		
	def on_submit(self):
		self.save(ignore_permissions=True)
		self.time = now()
		

		
			
		

	@frappe.whitelist()
	def get_data(self):
		
		bom_list = frappe.db.sql("""select * from `tabTSAI BOM` where fm ='%s' and depth = '2' and uom != '' """%(self.mat_number),as_dict=1)
		
		# bom_list = frappe.get_all('TSAI BOM',{'fm':self.mat_number},['*'])
		
		data = ''
		data += '<table class="table table-bordered" style="width:100%"><tr><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Mat Number</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Item Description</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>UOM</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Quantity</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Warehouse</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Depth</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Bom Type</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Warehouse Qty</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Print Qty</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Shortage Qty</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Status</b></center></td></tr>'

		for b in bom_list:
			warehouse_qty = get_live_stock(b.item)
			data += '<tr><td style="text-align:center;padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="text-align:center;padding:1px;border: 1px solid black;">%s</td><td style="text-align:center;text-align:center;padding:1px;border: 1px solid black;">%s</td><td style="text-align:center;padding:1px;border: 1px solid black;">%s</td><td style="text-align:center;padding:1px;border: 1px solid black;">%s</td><td style="text-align:center;padding:1px;border: 1px solid black;">%s</td><td style="text-align:center;padding:1px;border: 1px solid black;">%s</td><td style="text-align:center;padding:1px;border: 1px solid black;">%s</td>'%(b.item,b.item_description,b.uom,b.item_quantity,b.whse,b.depth,b.bom_type,warehouse_qty,self.quantity)

			if warehouse_qty < self.quantity:
				short_qty = warehouse_qty - self.quantity
				status = 'shortage'
				data += '<td style="padding:1px;text-align:center;background-color:#FF0000;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;text-align:center;background-color:#FF0000;border: 1px solid black;"><b>%s</b></td></tr>'%(short_qty,status)
				frappe.throw(_('Quantity Shortage'))
			else:
				short_qty = '-'
				status = 'ok'
				data += '<td style="padding:1px;border: 1px solid black;text-align:center;">%s</td><td style="text-align:center;padding:1px;border: 1px solid black;">%s</td></tr>'%(short_qty,status)
		return data

@frappe.whitelist()
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
				"select warehouse from `tabInventory Control Area` ", as_dict=True)

			wh_list = [d['warehouse'] for d in ica if 'warehouse' in d]

			df = pd.DataFrame(stocks)
			df = df[df['Warehouse'].isin(wh_list)]
			stock = pd.to_numeric(df["Qty"]).sum()
		return stock

@frappe.whitelist()
def get_shift_type():
	nowtime = datetime.now()
	shift_date = date.today()
	shift = frappe.db.get_value('Shift Type',{'name':'1'},['qr_start_time','qr_end_time'])
	shift1_time = [time(hour=shift[0].seconds//3600,minute=((shift[0].seconds//60)%60),second=0),time(hour=shift[1].seconds//3600,minute=((shift[1].seconds//60)%60),second=0)]
	frappe.errprint(shift1_time)
	# shift1_time = [time(hour=7, minute=0, second=0),time(hour=13, minute=30, second=0)]
	shift2_time = [time(hour=15, minute=30, second=0),time(hour=23, minute=30, second=0)]
	shift3_time = [time(hour=00, minute=0, second=1),time(hour=4, minute=0, second=0)]
	shiftpp2_time = [time(hour=23, minute=32, second=0),time(hour=23, minute=59, second=0)]
	# shiftpp1_time = [time(hour=7, minute=0, second=0),time(hour=10, minute=0, second=0)]
	# shift2_cont_time = [time(hour=22, minute=1, second=0),time(hour=22, minute=59, second=0)]
	curtime = time(hour=nowtime.hour, minute=nowtime.minute, second=nowtime.second)
	shift_type = '1'
	if is_between(curtime,shift1_time):
		shift_type = '1'
	if is_between(curtime,shift2_time):
		shift_type = '2'
	# if is_between(curtime,shift2_cont_time):
	#     shift_type = '2'
	if is_between(curtime,shift3_time):
		shift_type = '3'
		shift_date = shift_date + timedelta(days=-1)
	if is_between(curtime,shiftpp2_time):
		shift_type = 'PP2'
	
	return shift_type

def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]
