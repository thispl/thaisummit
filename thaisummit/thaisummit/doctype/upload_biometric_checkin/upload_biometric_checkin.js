// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Upload Biometric Checkin', {
	refresh: function(frm) {
		frappe.breadcrumbs.add("HR","Upload Biometric Checkin");
		if(frm.is_new()){
			frm.set_value("date",frappe.datetime.nowdate())
		}
		if(frm.doc.attach){
		frm.trigger('error_preview')
		}
		frm.add_custom_button(__('Re-Check'), function (){
			if(frm.doc.attach){
				frappe.call({
					method: "thaisummit.thaisummit.doctype.upload_biometric_checkin.upload_biometric_checkin.create_checkins",
					args: {
						"file": frm.doc.attach,
						"name":frm.doc.name
					},
					freeze: true,
					freeze_message: 'Uploading....',
					callback(r) {
						if(r){
							frappe.msgprint('Biometric Checkins has been uploaded sucessfully')
							frm.reload_doc()
						}
					}
				})
			}
		})
	},
	attach(frm){
		if(frm.doc.attach){
		frm.trigger('error_preview')
		}
	},
	error_preview(frm){
		frm.call('error_preview').then(r=>{
			if (r.message) {
				frm.fields_dict.error_preview.$wrapper.empty().append(r.message)
			}
		})
	},
	upload(frm){
		if(frm.doc.attach){
			frappe.call({
				method: "thaisummit.thaisummit.doctype.upload_biometric_checkin.upload_biometric_checkin.create_checkins",
				args: {
					"file": frm.doc.attach,
					"name":frm.doc.name
				},
				freeze: true,
        		freeze_message: 'Uploading....',
				callback(r) {
					if(r){
						frappe.msgprint('Biometric Checkins has been uploaded sucessfully')
						frm.reload_doc()
					}
				}
			})
		}
	},
});
