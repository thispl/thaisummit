// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Forecast', {
    refresh(frm){
        frm.disable_save()
        frappe.breadcrumbs.add("Home","E-KANBAN");
    },
    onload: function (frm) {
        frm.set_value('attach','')
        frm.set_value('from_date', frappe.datetime.month_start())
        frm.set_value('to_date', frappe.datetime.month_end())
        frm.trigger('show_data')
    },
    show_data(frm){
        frm.call({
            method: 'get_data',
            doc: frm.doc,
            freeze: true,
			freeze_message: __("Loading......"),
            callback: function (r) {
                if (r.message) {
                    frm.fields_dict.html.$wrapper.empty().append(r.message[0])
                    frm.fields_dict.summary.$wrapper.empty().append(r.message[1])
                }
            }
        });
    },
    form_date(frm){
        if(frm.doc.from_date && frm.doc.to_date){
        frm.trigger('show_data')
        }
    },
    to_date(frm){
        if(frm.doc.from_date && frm.doc.to_date){
        frm.trigger('show_data')
        }
    },
    download: function (frm) {
		window.location.href = repl(frappe.request.url +
			'?cmd=%(cmd)s&from_date=%(from_date)s&to_date=%(to_date)s', {
			cmd: "thaisummit.thaisummit.doctype.forecast.forecast.download",
            from_date: frm.doc.from_date,
			to_date: frm.doc.to_date,
		});
	},
    upload(frm){
		if(frm.doc.attach){
			frappe.call({
				method : 'thaisummit.thaisummit.doctype.forecast.forecast.enqueue_upload',
				args: {
					file: frm.doc.attach,
                    from_date : frm.doc.from_date,
                    to_date: frm.doc.to_date
				},
				freeze: true,
				freeze_message: 'Updating Forecast Data....',
				callback(r){
					if(r.message){
						frappe.show_alert({
							message:__('Forecast Data Updated Successfully'),
							indicator:'green'
						}, 5);
						frm.set_value('attach','')
                        frm.trigger('show_data')
					}
				}
			})
		}
		else{
			frappe.msgprint('Please Attach the Excel')
		}
	}
});
