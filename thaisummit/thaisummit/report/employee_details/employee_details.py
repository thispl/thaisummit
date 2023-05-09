# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

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
	columns, data = [], []
	columns=get_columns(filters)
	data=get_data(filters)
	return columns, data

def get_columns(filters):
	column=[
		_('Employee ID')+':Data:120',
	    _('Name')+':Data:120',
		_('Date Of Birth')+':Data:120',
	    #_('Status')+':Data:120',
	    _('Gender')+':Data:120',
	    _('Date Of Joining')+':Data:120',
		_('Department')+':Data:120',
		_('Designation')+':Data:120',
		_('Default Shift')+':Data:120',
		_('Employment Type')+':Data:120',
		_('Contractor')+':Data:120',
		_('Email')+':Data:120',
         ]
	return column


def get_data(filters):
	data = []
	employee_id= frappe.db.sql("""select * from `tabEmployee` where status = 'Active' """,as_dict=1)
	for t in employee_id:
		username= frappe.db.sql("""select email from `tabUser` where username = '%s' and enabled = '1' """%(t.employee_number),as_dict=1)
		for i in username:
			row=[t.employee_number,t.first_name,t.date_of_birth,t.gender,t.date_of_joining,t.department,t.designation,t.default_shift,t.employment_type,t.contractor,i.email]
			data.append(row)
	return data
