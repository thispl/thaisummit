// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Reports Dashboard', {
	// refresh: function(frm) {
	// 	frm.disable_save()
	// },
	download: function (frm) {
		if (frm.doc.report == 'Shift Schedule Summary Report') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.shift_schedule_summary_report.download"
			var args = 'date=%(date)s'
		}
		else if (frm.doc.report == 'CL Manpower Shortage Deduction Summary Report') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.cl_manpower_shortage_deduction_summary_report.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s'
		}
		else if (frm.doc.report == 'Monthly Individual Attendance Report') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.monthly_individual_attendance_report.download"
			var args = 'employee=%(employee)s&from_date=%(from_date)s&to_date=%(to_date)s'
		}
		else if (frm.doc.report == 'Monthly Manpower Plan vs Actual Report') {
			// var path = "thaisummit.thaisummit.doctype.reports_dashboard.monthly_manpower_plan_vs_actual_report.download"
			// var args = 'from_date=%(from_date)s&to_date=%(to_date)s'
			frm.set_value('attach','')
			frm.save();
			frappe.call({
				method : 'thaisummit.thaisummit.doctype.reports_dashboard.monthly_manpower_plan_vs_actual_report.download',
				args : {
					f_date : frm.doc.from_date,
					t_date : frm.doc.to_date,
				}
			})
		}
		else if (frm.doc.report == 'Monthly Manpower Report') {
			// var path = "thaisummit.thaisummit.doctype.reports_dashboard.monthly_manpower_report.download"
			// var args = 'from_date=%(from_date)s&to_date=%(to_date)s'
			frm.set_value('attach','')
			frm.save();
			frappe.call({
				method : 'thaisummit.thaisummit.doctype.reports_dashboard.monthly_manpower_report.download',
				args : {
					f_date : frm.doc.from_date,
					t_date : frm.doc.to_date
				}
			})
		}
		else if (frm.doc.report == 'Overall Monthly Manpower Report') {
			if(frappe.user.has_role('System Manager')){
			// var path = "thaisummit.thaisummit.doctype.reports_dashboard.overall_monthly_manpower_report.download"
			// var args = 'from_date=%(from_date)s&to_date=%(to_date)s'
			frm.set_value('attach','')
			frm.save();
			frappe.call({
				method : 'thaisummit.thaisummit.doctype.reports_dashboard.overall_monthly_manpower_report.download',
				args : {
					f_date : frm.doc.from_date,
					t_date : frm.doc.to_date
				}
			})
			}
			else{
				frappe.msgprint('Not Permitted')
			}
		}
		else if (frm.doc.report == 'Monthly Overtime Amount Report') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.monthly_overtime_amount_report.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s&employee_type=%(employee_type)s'
		}
		else if (frm.doc.report == 'Monthly Overtime Person Report') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.monthly_overtime_person_report.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s'
		}
		else if (frm.doc.report == 'Daily Sales Report') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.daily_sales_report.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s'
		}
		else if (frm.doc.report == 'Daily Sales Report Summary') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.daily_sales_report_summary.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s'
		}
		else if (frm.doc.report == 'Manpower Plan vs Actual Live Report (Shift Wise)') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.manpower_plan_vs_actual.download"
			var args = 'date=%(date)s&shift=%(shift)s'
		}
		else if (frm.doc.report == 'Delivery Plan vs Stock Report') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.delivery_plan_vs_stock_report.download"
		}
		else if (frm.doc.report == 'CL Overtime Report (Shift Continue)') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.cl_overtime_report.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s'
			// frm.set_value('attach','')
			// frm.save();
			// frappe.call({
			// 	method : 'thaisummit.thaisummit.doctype.reports_dashboard.cl_overtime_report.download',
			// 	args : {
			// 		f_date : frm.doc.from_date,
			// 		t_date : frm.doc.to_date,
			// 	}
			// })
		}
		else if (frm.doc.report == 'Payroll Cross Check Report') {
			frm.set_value('attach','')
			frm.save();
			if (frm.doc.employee_type){
			frappe.call({
				method : 'thaisummit.thaisummit.doctype.reports_dashboard.category_wise_report.download',
				args : {
					f_date : frm.doc.from_date,
					t_date : frm.doc.to_date,
					emp_type: frm.doc.employee_type
				}
			})
		}else{
			frappe.msgprint('Kindly choose Employee Type')
		}
		}
		else if (frm.doc.report == 'WC Salary Register') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.wc_salary_register.download"
			var args = 'employee_type=WC&from_date=%(from_date)s&to_date=%(to_date)s'
		}
		else if (frm.doc.report == 'BC Salary Register') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.bc_salary_register.download"
			var args = 'employee_type=BC&from_date=%(from_date)s&to_date=%(to_date)s'
		}
		else if (frm.doc.report == 'FT Salary Register') {
				var path = "thaisummit.thaisummit.doctype.reports_dashboard.ft_salary_register.download"
				var args = 'employee_type=ft&from_date=%(from_date)s&to_date=%(to_date)s'	
		}
		else if (frm.doc.report == 'NT Salary Register') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.nt_salary_register.download"
			var args = 'employee_type=nt&from_date=%(from_date)s&to_date=%(to_date)s'	
		}
		else if (frm.doc.report == 'CL Salary Register') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.cl_salary_register.download"
			var args = 'employee_type=nt&from_date=%(from_date)s&to_date=%(to_date)s'	
		}

		if (path) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path,
				args: args,
				date: frm.doc.date,
				from_date : frm.doc.from_date,
				to_date : frm.doc.to_date,
				employee : frm.doc.employee,
				shift : frm.doc.shift,
				employee_type: frm.doc.employee_type,
				department : frm.doc.department,
			});
		}
	},
	payroll_download(frm){
		if (frm.doc.payroll_reports == 'ESI Statement') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.esi_statement.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s'	
		}

		else if (frm.doc.payroll_reports == 'ESI and PF') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.esi_and_pf.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s'	
		}

		else if (frm.doc.payroll_reports == 'Cost Center Wise WC Wages') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.cost_center_wise_wc_wages.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s'	
		}
		else if (frm.doc.payroll_reports == 'Labour and Head cost') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.labour_and_head_cost.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s'	
		}

		if(path) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s',{
				cmd: path,
				args: args,
				employee_type : frm.doc.employee_type,
				from_date : frm.doc.from_date,
				to_date : frm.doc.to_date,
			});
		}
	}
});