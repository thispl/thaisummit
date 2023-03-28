// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bulk Upload Menu', {
    date:function(frm){
		var previous_day = frappe.datetime.add_days(frappe.datetime.now_date(),-1)
		if (frm.doc.date == previous_day ){
			frm.set_value('date','')
			frappe.throw(__('Past Date Should not be Allowed'))
		}
		
	}

});
