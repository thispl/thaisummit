// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('CL Reports', {
	// refresh: function(frm) {

	// }
	download: function (frm){
		if(frm.doc.reports == 'CL Reports Contractor Wise'){
			var path = "thaisummit.thaisummit.doctype.cl_reports.cl_wages_contractor_wise.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s&contractor=%(contractor)s'
		}

		else if(frm.doc.reports == 'CL Manpower Summary'){
			var path = "thaisummit.thaisummit.doctype.cl_reports.cl_manpower_summary.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s&contractor=%(contractor)s'
		}
		else if(frm.doc.reports == 'CL Monthly OT Register'){
			// var path = "thaisummit.thaisummit.doctype.cl_reports.cl_monthly_ot_register.download"
			// var args = 'from_date=%(from_date)s&to_date=%(to_date)s'
			frm.set_value('attach','')
			frm.save();
			frappe.call({
				method : 'thaisummit.thaisummit.doctype.cl_reports.cl_monthly_ot_register.download',
				args : {
					f_date : frm.doc.from_date,
					t_date : frm.doc.to_date,
				}
			})
		}


		if (path) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path,
				args: args,
				from_date : frm.doc.from_date,
				to_date : frm.doc.to_date,
				contractor : frm.doc.contractor,
			});
		}

	}
});
