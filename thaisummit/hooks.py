# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "thaisummit"
app_title = "Thaisummit"
app_publisher = "TEAMPRO"
app_description = "Customizations for Thai summit"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "erp@groupteampro.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# Scheduled Tasks
# ---------------
# doc_events = {
# 	"Leave Allocation":{
# 		"after_submit":"thaisummit.utils.create_leave",
		
# 	}
# }
scheduler_events = {
# 	"all": [
# 		"thaisummit.tasks.all"
# 	],
	# "daily": [
	# 	"thaisummit.custom.test_hook",
	# 	"thaisummit.custom.send_mail_hr",
	# 	"thaisummit.custom.create_leave_allocation",
	# 	"thaisummit.custom.delete_shift_summary"
	# ],
	# "hourly": [
	# 	"thaisummit.custom.test_hook"
	# ],
# 	"weekly": [
# 		"thaisummit.tasks.weekly"
# 	]
# 	"monthly": [
# 		"thaisummit.tasks.monthly"
# 	]
	# "weekly": [
    #     "thaisummit.custom.mail_wc_get_trainee",
    #     "thaisummit.custom.mail_wc_get_probation",
    #     "thaisummit.custom.mail_wc_probation"
	# ],
	# "yearly": [
	# 	"thaisummit.custom.el_leave_policy",
	# 	"thaisummit.custom.el_leave_encashment"
	# ],
	"cron": {
		"* * * * *": [
            "thaisummit.custom.test_hook"
        ],
        # "0 1 * * *": [
        #     "thaisummit.custom.fetch_sap_stock"
        # ],
		# "5 0 1 * *": [
        #     "thaisummit.custom.mark_deductions"
        # ],
		# "0 9 * * *": [
		# 	"thaisummit.custom.bulk_mail_alerts"
		# ],
		# "0 3 * * *":[
		# 	"thaisummit.custom.update_shift_status"
		# ]
	}
}

# include js, css files in header of desk.html
# app_include_css = "/assets/thaisummit/css/thaisummit.css"
app_include_js = "/assets/thaisummit/js/thaisummit.js"

# include js, css files in header of web template
# web_include_css = "/assets/thaisummit/css/thaisummit.css"
# web_include_js = "/assets/thaisummit/js/thaisummit.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "thaisummit/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "thaisummit.install.before_install"
# after_install = "thaisummit.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "thaisummit.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Salary Slip": "thaisummit.overrides.CustomSalarySlip",
	"Payroll Entry": "thaisummit.overrides.CustomPayrollEntry",
	"Shift Assignment": "thaisummit.overrides.CustomShiftAssignment",
	"Leave Application": "thaisummit.overrides.CustomLeaveApplication",
	"Compensatory Leave Request": "thaisummit.overrides.CustomCompensatoryLeaveRequest",
	"Employee":"thaisummit.overrides.CustomEmployee",
	"Additional Salary":"thaisummit.overrides.CustomAdditionalSalary"
	# "Overtime Request":"thaisummit.overrides.CustomOvertimeRequest",
}

jenv = {
	"methods": [
		"get_dispatch_data:thaisummit.custom.get_dispatch_data",
		"manpower_attendance_report:thaisummit.thaisummit.doctype.manpower_attendance_report.manpower_attendance_report.manpower_attendance_report",
		"manpower_attendance_report_total:thaisummit.thaisummit.doctype.manpower_attendance_report.manpower_attendance_report.manpower_attendance_report_total",
		"shift_wise_count:thaisummit.thaisummit.doctype.shift_schedule.shift_schedule.shift_wise_count",
		"shift_employees:thaisummit.thaisummit.doctype.shift_schedule.shift_schedule.shift_employees",
		"get_shift_status:thaisummit.thaisummit.doctype.shift_schedule_status_summary.shift_schedule_status_summary.get_shift_status",
		"get_dates:thaisummit.thaisummit.doctype.monthly_sales_per_head.monthly_sales_per_head.get_dates",
		"get_att_count:thaisummit.thaisummit.doctype.monthly_sales_per_head.monthly_sales_per_head.get_att_count",
		"get_total_count:thaisummit.thaisummit.doctype.monthly_sales_per_head.monthly_sales_per_head.get_total_count",
		"get_support_att_count:thaisummit.thaisummit.doctype.monthly_sales_per_head.monthly_sales_per_head.get_support_att_count",
		"get_grand_total:thaisummit.thaisummit.doctype.monthly_sales_per_head.monthly_sales_per_head.get_grand_total",
		"get_ot_amt:thaisummit.thaisummit.doctype.ot_sales_report.ot_sales_report.get_ot_amt",
		"get_ot_total:thaisummit.thaisummit.doctype.ot_sales_report.ot_sales_report.get_ot_total",
		"get_cl_count:thaisummit.thaisummit.print_format.cl_headcount_plan.cl_headcount_plan.get_cl_count",
	]
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Employee": {
		"on_update":[ 
			"thaisummit.custom.delete_left_att",
			"thaisummit.custom.mark_biometric_pin"

		]

		# "on_cancel": "method",
		# "on_trash": "method"
	},
	"IYM Sequence Plan Upload":{
		'on_submit': "thaisummit.thaisummit.doctype.tsa_master.tsa_master.enqueue_master_creation"
	},
	"TSAI Invoice":{
		'after_insert':[
			"thaisummit.api.push_invoice",

		],
		'on_update': "thaisummit.custom.get_gst_percent"


	},
	# 'Tag Card':{
	# 	'after_insert': "thaisummit.thaisummit.doctype.generate_tag_card.generate_tag_card.link_document_name"
	# },
	
}

# Testing
# -------

# before_tests = "thaisummit.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "thaisummit.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "thaisummit.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

fixtures = ['Custom Field','Workspace']


