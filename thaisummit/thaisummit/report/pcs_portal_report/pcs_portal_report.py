# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

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
from datetime import datetime, timedelta
from datetime import datetime, timedelta
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
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
	_('Customer') + ':Data:180',
	_('Vendor Code') + ':Data:180',
	_('Vendor Name') + ':Data:180',
	_('Item Code') + ':Data:180',
	_('Part No') + ':Data:180',
	_('Item Description') + ':Data:180',
	_('Model') + ':Data:180',
	_('Grade') + ':Data:180',
	_('MAT Type') + ':Data:180',
	_('Size Type') + ':Data:180',
	_('RM Length') + ':Data:180',
	_('RM Width') + ':Data:180',
	_('RM Thick') + ':Data:180',
	_('Strip Qty') + ':Data:180',
	_('Gross Weight') + ':Data:180',
	_('Net Weight') + ':Data:180',
	_('Scrap Weight') + ':Data:180',
	_('RM Price') + ':Data:180',
	_('Gross WT Cost') + ':Data:180',
	_('Scrap Cost/kg') + ':Data:180',
	_('Scrap Cost') + ':Data:180',
	_('RM Cost') + ':Data:180',
	_('Process Cost') + ':Data:180',
	_('Admin Cost') + ':Data:180',
	_('Transport Cost') + ':Data:180',
	_('Final Part Cost') + ':Data:180',

	]
	return columns

def get_data(filters):
	data = []
	pcs_part_master = frappe.db.sql("""select * from `tabPCS Part Master` """,as_dict=1)
	scrap_weight = 0
	scrap_cost = 0
	final_part_cost = 0
	for p in pcs_part_master:
		scrap_master = frappe.db.sql("""select iym from `tabScrap Master` where vendor_code = '%s' """%(p.vendor_code),as_dict=1)
		for s in scrap_master:
			gross_weight = float(p.gross_weight)
			net_weight = float(p.net_weight)
			scrap_weight = round((gross_weight - net_weight),3)
			scrap_cost = round((scrap_weight * float(s.iym)),3)
			final_part_cost = round((float(p.process_cost) + float(p.admin_cost) + float(p.admin_cost) + float(p.transport_cost)),3)
			row =[p.customer,p.vendor_code,p.vendor_name,p.item_code,p.part_no,p.item_description or '',p.model,p.grade,p.mat_type,p.size_type,p.rm_length,p.rm_width,p.rm_thick,p.strip_qty,round(float(p.gross_weight),3),p.net_weight,scrap_weight,"","",s.iym or '0',scrap_cost,"",round(float(p.process_cost),3),round(float(p.admin_cost),3),round(float(p.transport_cost),3),final_part_cost]
			data.append(row)
	return data





