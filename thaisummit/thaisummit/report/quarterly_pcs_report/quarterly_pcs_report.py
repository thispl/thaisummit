# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe

# import frappe
from frappe.model.document import Document
import datetime
import frappe
from frappe.model.document import Document
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
from itertools import count
import frappe
from frappe import permissions
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
from math import floor
from frappe import msgprint, _
from calendar import month, monthrange
from datetime import date, timedelta, datetime,time
from numpy import true_divide
import pandas as pd
import datetime as dt


def execute(filters=None):
	columns, data = [] ,[]
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	column = [
		_('Card Name') + ':Data:150',
		_('Mat No') + ':Data:150',
		_('Parts No') + ':Data:190',
		_('Model') + ':Data:150',
        _('Item Description') + ':Data:150',
		_('Grade') + ':Data:220',
		_('New RM Price') + ':Float:220',
		_('New RM Cost') + ':Float:220',
		_('New Process Cost') + ':Float:220',
		_('New Admin Codt') + ':Float:220',
		_('New Transport Cost') + ':Float:220',
		_('New Total Cost') + ':Float:220',
		_('Old RM Price') + ':Float:220',
		_('Old RM Cost') + ':Float:220',
		_('Old Process Cost') + ':Float:220',
		_('Old Admin Codt') + ':Float:220',
		_('Old Transport Cost') + ':Float:220',
		_('Old Total Cost') + ':Float:220',
		_('Difference RM Price') + ':Float:220',
		_('Difference RM Cost') + ':Float:220',
		_('Difference Process Cost') + ':Float:220',
		_('Difference Admin Codt') + ':Float:220',
		_('Difference Transport Cost') + ':Float:220',
		_('Part Cost') + ':Float:220'

	]
	return column

def get_data(filters):
	data = []
	pcs_master = frappe.db.sql("""select * from `tabPCS Part Master` """,as_dict=1)
	new_rm_price = 0
	rm_cost = 0
	gross_wt_cost = 0
	gross_weight = 0
	net_weight = 0
	scrap_weight = 0
	scrap_cost = 0
	rm_cost = 0
	old_gross_weight = 0
	old_net_weight = 0
	old_gross_wt_cost = 0
	old_scrap_weight = 0
	old_scrap_cost = 0
	old_rm_cost = 0
	old_rm_price = 0
	for p in pcs_master:
		rm_price_iym = frappe.get_single('RM Input').rm_input_table1
		rm_price_re = frappe.get_single('RM Input').rm_input_table2
		if p.customer == "IYM":
			for r in rm_price_iym:
				if p.grade == r.grade:
					if p.size_type == ">100":
						new_rm_price = r.new1
					elif p.size_type == "<100":
						new_rm_price = r.new2
					else:
						new_rm_price = 0
			scrap_master = frappe.get_single('PCS Scrap Master').scrap_master
			for s in scrap_master:
				gross_weight = float(p.gross_weight)
				net_weight = float(p.net_weight)
				gross_wt_cost = round((gross_weight * new_rm_price ),3)
				scrap_weight = round((gross_weight - net_weight),3)
				scrap_cost = round((scrap_weight * float(s.iym)),3)
				rm_cost = round((gross_wt_cost - scrap_cost),3)
		elif p.customer == "RE":
			for r in rm_price_re:
				if p.grade == r.grade:
					if p.mat_type == 'STRIP':
						if p.size_type == ">100":
							new_rm_price = r.new1
						elif p.size_type == "<100":
							new_rm_price = r.new2
						else:
							new_rm_price = 0
					elif p.mat_type == 'COIL':
						if p.size_type == ">100":
							new_rm_price = r.coil_new
						elif p.size_type == "<100":
							new_rm_price = r.coil_new1
						else:
							new_rm_price = 0
			scrap_master = frappe.get_single('PCS Scrap Master').scrap_master
			for s in scrap_master:
				gross_weight = float(p.gross_weight)
				net_weight = float(p.net_weight)
				gross_wt_cost = round((gross_weight * new_rm_price),3)
				scrap_weight = round((gross_weight - net_weight),3)
				scrap_cost = round((scrap_weight * float(s.re)),3)
				rm_cost = round((gross_wt_cost - scrap_cost),3)

		rm_price_iym_old = frappe.get_single('RM Input').old_iym_settings
		rm_price_re_old = frappe.get_single('RM Input').old_re_settings
		if p.customer == "IYM":
			for r in rm_price_iym_old:
				if p.grade == r.grade:
					if p.size_type == ">100":
						old_rm_price = r.new1
					elif p.size_type == "<100":
						old_rm_price = r.new2
					else:
						old_rm_price = 0
			scrap_master = frappe.get_single('PCS Scrap Master').scrap_master
			for s in scrap_master:
				old_gross_weight = float(p.gross_weight)
				old_net_weight = float(p.net_weight)
				old_gross_wt_cost = round((old_gross_weight * old_rm_price ),3)
				old_scrap_weight = round((old_gross_weight - old_net_weight),3)
				old_scrap_cost = round((old_scrap_weight * float(s.iym)),3)
				old_rm_cost = round((old_gross_wt_cost - old_scrap_cost),3)
		elif p.customer == "RE":
			for r in rm_price_re_old:
				if p.grade == r.grade:
					if p.mat_type == 'STRIP':
						if p.size_type == ">100":
							old_rm_price = r.new1
						elif p.size_type == "<100":
							old_rm_price = r.new2
						else:
							old_rm_price = 0
					elif p.mat_type == 'COIL':
						if p.size_type == ">100":
							old_rm_price = r.coil_new
						elif p.size_type == "<100":
							old_rm_price = r.coil_new1
						else:
							old_rm_price = 0
			scrap_master = frappe.get_single('PCS Scrap Master').scrap_master
			for s in scrap_master:
				old_gross_weight = float(p.gross_weight)
				old_net_weight = float(p.net_weight)
				old_gross_wt_cost = round((old_gross_weight * old_rm_price ),3)
				old_scrap_weight = round((old_gross_weight - old_net_weight),3)
				old_scrap_cost = round((old_scrap_weight * float(s.re)),3)
				old_rm_cost = round((old_gross_wt_cost - old_scrap_cost),3)
		row = [p.vendor_name,p.name,p.part_no,p.model,p.parts_name,p.grade,new_rm_price,
		rm_cost,p.process_cost,p.admin_cost,p.transport_cost,(rm_cost + p.process_cost + p.admin_cost + p.transport_cost),
		old_rm_price,old_rm_cost,p.process_cost,p.admin_cost,p.transport_cost,
		(old_rm_cost + p.process_cost + p.admin_cost + p.transport_cost),(new_rm_price - old_rm_price),(rm_cost - old_rm_cost),
		(p.process_cost - p.process_cost),(p.admin_cost - p.admin_cost),(p.transport_cost - p.transport_cost),
		((rm_cost + p.process_cost + p.admin_cost + p.transport_cost) - (old_rm_cost + p.process_cost + p.admin_cost + p.transport_cost))]
		data.append(row)
	return data

