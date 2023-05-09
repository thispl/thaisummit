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
		_('ENQUEUE BACKGROUND JOBS') + ':Data:700',
		_('STATUS') + ':Data:200',
		_('CREATED TIME') + ':Data:200',


	]
	return column

def get_data(filters):
	data = []
	import redis
	from rq import Queue,Worker
	from frappe.utils.background_jobs import get_redis_conn
	from frappe.utils import convert_utc_to_user_timezone, format_datetime

	conn = get_redis_conn()
	queues = Queue.all(conn)
	workers = Worker.all(conn)
	jobs = []
	def add_job(job: 'Job', name: str) -> None:
		if job.kwargs.get('site') == frappe.local.site:
			job_info = {
				'job_name':job.kwargs.get('kwargs', {}).get('playbook_method') or
					job.kwargs.get('kwargs', {}).get('job_type')
					or str(job.kwargs.get('job_name')),
				'status': job.get_status(),
				'queue': name,
				'creation': format_datetime(convert_utc_to_user_timezone(job.created_at))
			}

			if job.exc_info:
				job_info['exc_info'] = job.exc_info
			jobs.append(job_info)

	for worker in workers:
		job = worker.get_current_job()
		if job:
			add_job(job, worker.name)

	for queue in queues:
		if queue.name != 'failed':
			for job in queue.jobs:
				add_job(job, queue.name)
	for j in jobs:
		row = [str(j['job_name']),j['status'],j['creation']] or '-'
		frappe.errprint((j['job_name']))
		data.append(row)
	return data
	return jobs

