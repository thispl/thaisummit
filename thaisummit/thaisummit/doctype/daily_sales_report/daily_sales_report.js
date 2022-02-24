// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Sales Report', {
	refresh: function(frm) {
		frm.disable_save()
        frappe.breadcrumbs.add("Home","E-KANBAN");
		frm.set_value('from_date',frappe.datetime.month_start())
		frm.set_value('to_date',frappe.datetime.month_end())
        // frm.set_value('from_date','2021-10-01')
		// frm.set_value('to_date','2021-10-31')
	},
    show_data(frm){
        frm.call({
            method: 'get_data',
            doc: frm.doc,
            freeze: true,
			freeze_message: __("Loading......"),
            callback: function (r) {
                if (r.message) {
                    frm.fields_dict.html.$wrapper.empty().append(r.message)
                }
            }
        });
    },
    // from_date(frm){
    //     if(frm.doc.from_date && frm.doc.to_date){
    //     frm.trigger('show_data')
    //     }
    // },
    view(frm){
        if(frm.doc.from_date && frm.doc.to_date){
        frm.trigger('show_data')
        }
    },
    download(frm){
        if (frm.doc.from_date && frm.doc.to_date) {
			var path = "thaisummit.thaisummit.doctype.reports_dashboard.daily_sales_report.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s'	
		}
        else{
            frappe.msgprint('Please Fill From Date & To Date')
        }
        if (path) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path,
				args: args,
				from_date : frm.doc.from_date,
				to_date : frm.doc.to_date,
			});
		}
    }
});