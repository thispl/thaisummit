# Copyright (c) 2023, TEAMPRO and contributors
# For license information, please see license.txt

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
from operator import itemgetter
from frappe import _

class TagCard(Document):
	def on_submit(self):
		user = frappe.session.user
		u_name = frappe.db.sql("""select username from `tabUser` where name='%s' """%(frappe.session.user),as_dict=1)[0]
		if user == 'gururaja528@gmail.com':
			self.append('workflow_tracker_table',{
				'flow_name': "Closed by Rajaguru",
				'time':datetime.now().strftime('%H:%M:%S'),
				'date':date.today(),
				'user_name':u_name['username']
			})
			self.save()
			self.submit()


	def on_update(self):
		part_master = frappe.db.sql("""select tag_card_flow_master as tc from `tabTSAI Part Master` where mat_no ='%s' """%(self.mat_number),as_dict=1)[0]
		name_f = part_master['tc']
		doc = frappe.get_doc('Tag Card Flow Master', name_f)
		# Get the list of child rows
		children = doc.get('tag_card_workflow_table')
		if self.current_workflow == children[-1].workflow:
			self.submit()

	def validate(self):
		if self.current_workflow != 'Rejected':
			self.workflow_changing_date_and_time = datetime.now().strftime('%H:%M:%S')
			
		part_master = frappe.db.sql("""select tag_card_flow_master as tc from `tabTSAI Part Master` where mat_no ='%s' """%(self.mat_number),as_dict=1)[0]
		name_f = part_master['tc']
		doc = frappe.get_doc('Tag Card Flow Master', name_f)
		# Get the list of child rows
		children = doc.get('tag_card_workflow_table')
		self.set('workflow_table', [])
		# Loop through the child rows
		for child_row in children:
			# Get the workflow name from the child row
			workflow_name = child_row.workflow
			role_name = child_row.role_name
			allowed_for = child_row.allowed_for
			self.append('workflow_table',{
				'workflow':workflow_name,
				'role_name':role_name,
				'allowed_for':allowed_for
			})


@frappe.whitelist()
def update_list():
	prod_line_emp = []
	user = frappe.session.user
	if user not in ['Administrator','gururaja528@gmail.com']:
		emp_details = frappe.db.sql("""select name from `tabEmployee Production Line Details` where user_id ='%s' """%(user),as_dict=1)[0]
		emp_name = emp_details['name']
		emp_doc = frappe.get_doc('Employee Production Line Details', emp_name)
		emp_prod_line = emp_doc.get('production_line')
		for e in emp_prod_line:
			prod_line_emp.append(e.production_line_no)
		return prod_line_emp


@frappe.whitelist()
def update_workflow_list():
	actual_flow = []
	user = frappe.session.user
	if user not in ['Administrator','gururaja528@gmail.com']:
		user_roles = frappe.get_roles(user)
		tag_card = frappe.db.sql("""select name from `tabTag Card`""",as_dict=1)
		for t in tag_card:
			work_flow = frappe.get_doc('Tag Card', t.name)
			flow_line = work_flow.get('workflow_table')
			if flow_line:
				for f in flow_line:
					if (f.allowed_for in user_roles):
						actual_flow.append(f.allowed_for)
						frappe.errprint(f.allowed_for)
						return actual_flow


			
		
		
