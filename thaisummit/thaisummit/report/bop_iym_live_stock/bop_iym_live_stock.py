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
		_('Packing Std') + ':Data:120',
		_('Daily Order') + ':Data:120',
		_('Max Day') + ':Data:120',
		_('Max Stock') + ':Data:120',
		_('Min Day') + ':Data:120',
		_('Min Stock') + ':Data:120',
		_('Live Stock') + ':Data:120',
		_('Coverage Day') + ':Data:120',
		_('Req') + ':Data:120',
		_('Prod Plan') + ':Data:120',
	
	]
	return column


@frappe.whitelist()
def get_tag_list():
	total_tbs = frappe.db.sql("""select * from `tabTSAI Part Master` where mat_type in ('INH'&'BOP') and customer ='IYM' """,as_dict=1)
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
			updated_tbs_dict['parts_name'] = (tbs['parts_name'])
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
			updated_tbs_dict['prod_plan'] = get_open_production_qty(tbs['mat_no'])
			updated_tbs_list.append(updated_tbs_dict.copy())
			count += 1

	current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")
	updated_tbs_list = sorted(updated_tbs_list, key=lambda d: d['coverage_day'])
	data = [updated_tbs_list, current_datetime]
	return updated_tbs_list




def get_open_production_qty(mat_no):
	qty = 0
	from datetime import date
	today = date.today()
	openqty = frappe.get_value('Open Production Order',{'daily_order_date':today,'mat_no':mat_no},['open_qty'])
	if openqty:
		qty = flt(openqty)
	return qty



def get_live_stock(mat_no):
	qty = 0
	from datetime import date
	today = date.today()
	stock1 = frappe.get_value('Live Stock Quantity',{'live_stock_date':today,'mat_no':mat_no},['stock'])
	if stock1:
		qty = flt(stock1)
	return qty