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
		if (frm.doc.report == 'Monthly Individual Attendance Report') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.monthly_individual_attendance_report.download"
			var args = 'employee=%(employee)s&from_date=%(from_date)s&to_date=%(to_date)s'
		}
		if (frm.doc.report == 'Monthly Manpower Report') {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.monthly_manpower_report.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s'
		}
		if (path) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path,
				args: args,
				date: frm.doc.date,
				from_date : frm.doc.from_date,
				to_date : frm.doc.to_date,
				employee : frm.doc.employee
			});
		}
	},
});

