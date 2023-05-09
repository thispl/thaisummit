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
from datetime import datetime, timedelta


def execute(filters=None):
	columns, data = [] ,[]
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	
	columns = [
	_('Tag Card Name') + ':Data:180',
	_('Generated Date') + ':Date:150',
	_('Generated Time') + ':Data:190',
	_('Mat Number') + ':Data:180',
	_('Part Number') + ':Data:180',
	_('Part Name') + ':Data:180',
	_('Production Line') + ':Data:180',
	_('Open by production') + ':Data:220',
	_('Confirmed By QA') + ':Data:220',
	_('Confirmed By PDI') + ':Data:220',
	_('Received By Sales') + ':Data:220',
	_('Received by PPC before Job Work') + ':Data:220',
	_('Received by PPC after Job Work') + ':Data:220',
	_('Confirmed by IQA') + ':Data:220',
	_('Time difference between Workflows') + ':Data:220',


	]

	return columns



def get_data(filters):
	data = []
	unique_rows = set()
	if filters.tag_card:
		tag_card = frappe.db.sql("""select * from `tabTag Card` where date between '%s' and '%s' and name = '%s' """%(filters.from_date,filters.to_date,filters.tag_card),as_dict=1)
	else:
		tag_card = frappe.db.sql("""select * from `tabTag Card` where date between '%s' and '%s' """%(filters.from_date,filters.to_date),as_dict=1)

	for t in tag_card:
		tag_doc = frappe.get_doc("Tag Card", t.name)
		flow_table = tag_doc.get('workflow_tracker_table')
		prev_time = None
		time = '-'
		time_confirmed = '-' 
		pdi_time = '-' 
		sales_time = '-' 
		before_j_w = '-'
		after_j_w = '-'
		iqa_time = '-'
		time_ = '-'
		for f in flow_table:
			current_time = datetime.strptime(f.time, "%H:%M:%S")
			time_diff = None
			if prev_time:
				time_diff = current_time - prev_time
			if f.flow_name == 'Open By Production':
				time = f.user_name + ' ' +f.date + ' ' +f.time
			elif f.flow_name == 'Confirmed By QA':
				time_confirmed = f.user_name + ' ' +f.date + ' ' +f.time
			elif f.flow_name == 'Confirmed By PDI':
				pdi_time = f.user_name + ' ' +f.date + ' ' +f.time
			elif f.flow_name == 'Received By Sales':
				sales_time = f.user_name + ' ' +f.date + ' ' +f.time
			elif f.flow_name == 'Received by PPC before Job Work':
				before_j_w = f.user_name + ' ' +f.date + ' ' +f.time
			elif f.flow_name == 'Received by PPC after Job Work':
				after_j_w = f.user_name + ' ' +f.date + ' ' +f.time
			elif f.flow_name == 'Confirmed by IQA':
				iqa_time = f.user_name + ' ' +f.date + ' ' +f.time

			prev_time = current_time
			if time_diff:
				time_ += str(time_diff) + ',' + ' '

		row = (t.name, t.date, t.time, t.mat_number, t.part_number, t.mat_name, t.quantity,time,time_confirmed,pdi_time,sales_time,before_j_w,after_j_w,iqa_time,time_)
		if row not in unique_rows:
			data.append(row)
			unique_rows.add(row)

	return data

