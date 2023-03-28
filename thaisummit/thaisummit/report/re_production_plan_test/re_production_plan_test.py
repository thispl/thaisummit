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
		_('Today Headcount After Adj') + ':Float:120',
		_('Today Hr After Adj') + ':Data:120',
		_('Total Qty') + ':Data:120',
		_('total headcount') + ':Data:120',
		_('Total Hr') + ':Float:120',
		_('Check') + ':Data:120',
		_('Mat Number') + ':Data:120',
		_('Qty Today') + ':Data:120',
		_('Doc Date') + ':Data:120',


		
	
	]
	return column


@frappe.whitelist()
def get_tag_list():
	
	updated_tbs_list = []
	updated_tbs_dict = {}
	pr_name = frappe.db.get_value(
		'Prepared Report', {'report_name': 'RE Production Plan', 'status': 'Completed'}, 'name')

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
	# frappe.log_error(dos)

	#taking[:-1]for avoiding total row in prepared report
	sum = 0
	for do in dos[:-1]:
		sum += do['today_headcount_after_adj']
	frappe.log_error(sum)
	for do in dos[:-1]:
		sum_today_qty = do['today_qty']
	for do in dos[:-1]:
		sum_adj_today_qty_witout_percent = do['today_qty_after_adj']
	# for do in dos[:-1]:
		
	for do in dos[:-1]:
		tody_qty = 0
		man_power = frappe.get_single('Ekanban Settings').iym_manpower_limit
		percentage = [100,95,90,85,80,75,70,65,60,55,50,45,40,35]
		today_qty = do['today_qty_after_adj']
		packing_std = do['packing_std']
		for p in percentage:
			# if man_power > sum:
				# if sum_today_qty > sum_adj_today_qty_witout_percent:
			adj_percent = (p / 100)
			frappe.log_error(adj_percent)
		tody_qty = round((today_qty * adj_percent) / packing_std)*packing_std
		
		mat_number = do['mat_no']
		t_qty = tody_qty
		date_today = date.today()
		date_string = date_today.strftime("%Y-%m-%d")
		new_date_string = date_string.replace("-", "")

		# if do['unit_per_shift'] > 0 :
		# 	today_headcount1 = round((tody_qty / (do['unit_per_shift'])) * do['manpower_std'],2)
		
		total_qty = tody_qty + do['pending_qty']
		
		
	
		updated_tbs_dict['mat_no'] = do['mat_no']
		updated_tbs_dict['parts_name'] = (do['parts_name'])
		updated_tbs_dict['parts_no'] = do['parts_no']
		updated_tbs_dict['mat_type'] = (do['mat_type'])
		updated_tbs_dict['model'] = do['model']
		updated_tbs_dict['production_line'] = do['production_line'] 
		updated_tbs_dict['customer'] = do['customer']
		updated_tbs_dict['manpower_std'] = do['manpower_std']
		updated_tbs_dict['cycle_time'] = do['cycle_time']
		updated_tbs_dict['uph'] = do['uph']
		updated_tbs_dict['unit_per_shift'] = do['unit_per_shift']
		updated_tbs_dict['packing_std'] = do['packing_std']
		updated_tbs_dict['daily_order'] = do['daily_order']
		updated_tbs_dict['max_day'] = do['max_day']
		updated_tbs_dict['max_qty'] = do['max_qty']
		updated_tbs_dict['min_day'] = do['min_day']
		updated_tbs_dict['min_qty'] = do['min_qty']
		updated_tbs_dict['live_stock'] = do['live_stock']
		updated_tbs_dict['coverage'] = do['coverage']
		updated_tbs_dict['pending_qty'] = do['pending_qty']
		updated_tbs_dict['require_qty'] = do['require_qty']
		updated_tbs_dict['require_headcount'] = do['require_headcount']
		updated_tbs_dict['required_hr'] = do['required_hr']
		updated_tbs_dict['cap'] = do['cap']
		updated_tbs_dict['pending_headcount'] = do['pending_headcount']
		updated_tbs_dict['pending_hr'] = do['pending_hr']
		updated_tbs_dict['today_qty'] = do['today_qty']
		updated_tbs_dict['today_headcount'] = do['today_headcount']
		updated_tbs_dict['today_hr'] = do['today_hr']
		updated_tbs_dict['today_qty_after_adj'] = tody_qty
		if do['unit_per_shift'] > 0 :
			today_headcount1 = round((tody_qty / (do['unit_per_shift'])) * do['manpower_std'],2)
			updated_tbs_dict['today_headcount_after_adj'] = today_headcount1
		else:
			updated_tbs_dict['today_headcount_after_adj'] = 0

		if do['uph'] > 0:
			today_hr1 = round((today_headcount1 / do['uph']),2)
			updated_tbs_dict['today_hr_after_adj'] = today_hr1
		else:
			updated_tbs_dict['today_hr_after_adj'] = 0

		updated_tbs_dict['total_qty'] = total_qty
		if do['unit_per_shift'] > 0 :
			total_headcount = round((total_qty / do['unit_per_shift']) * do['manpower_std'],2)
			updated_tbs_dict['total_headcount'] = total_headcount
		else:
			updated_tbs_dict['total_headcount'] = 0

		if do['uph'] > 0:
			total_hr = round((total_qty / do['uph']),2)
			updated_tbs_dict['total_hr'] = total_hr
		else:
			updated_tbs_dict['total_hr'] = 0

		updated_tbs_dict['check'] = do['check']
		if tody_qty > 0:
			updated_tbs_dict['mat_number'] = mat_number
			updated_tbs_dict['qty_today'] = t_qty
			updated_tbs_dict['doc_date'] = new_date_string
		else:
			updated_tbs_dict['mat_number'] = '-'
			updated_tbs_dict['qty_today'] = '-'
			updated_tbs_dict['doc_date'] = '-'



		updated_tbs_dict['coverage_day'] = do['coverage_day']
		updated_tbs_list.append(updated_tbs_dict.copy())
	current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")
	updated_tbs_list = sorted(updated_tbs_list, key=lambda d: d['coverage_day'])
	tqty = []
	
	data = [updated_tbs_list]

	
	return updated_tbs_list


# head_count = do['today_headcount_after_adj']
#         man_power = frappe.get_single('Ekanban Settings').iym_manpower_limit
#         percentage = 0.9
#         if man_power < head_count:
#             tody_qty = head_count * percentage

