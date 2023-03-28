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
		_('Tag Card Name') + ':Data:120',
		_('Generated Date') + ':Date:150',
		_('Generated Time') + ':Data:190',
		_('Mat Number') + ':Data:120',
        _('Part Number') + ':Data:120',
		_('Part Name') + ':Data:220',
		_('Production Line') + ':Data:220',
		_('Model') + ':Data:100',
		_('Standard Quantity') + ':Data:150',
		_('Time Elapsed') + ':Data:150',
		# _('Current Workflow State') + ':Data:200',
		_('Status') + ':Data:150'

	]
	return column

def get_data(filters):
	data = []
	tag_card = frappe.db.sql("""select * from `tabTag Card` where docstatus = 0 and previous_workflow != '' """,as_dict=1)
	for t in tag_card:
		part_master = frappe.db.sql("""select production_line,model from `tabTSAI Part Master` where mat_no ='%s' """%(t.mat_number),as_dict =1)
		formatted_dt = t.creation.strftime("%Y-%m-%d %H:%M:%S")
		current_datetime =  datetime.now()
		formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
		datetime_obj1 = datetime.strptime(formatted_dt, "%Y-%m-%d %H:%M:%S")
		datetime_obj2 = datetime.strptime(formatted_datetime, "%Y-%m-%d %H:%M:%S")
		open_days = datetime_obj2 - datetime_obj1
		for p in part_master:
			prod = p.production_line
			mod = p.model
		if t.previous_workflow != ('Completed'):
			row = [t.name,t.date,t.time,t.mat_number,t.part_number,t.mat_name,prod,mod,t.quantity,open_days,t.previous_workflow or '-']
		data.append(row)
	return data

