// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Ekanban Settings', {
	refresh: function (frm) {
		frm.disable_save()
		frm.set_value('date', frappe.datetime.get_today())
		frm.set_value('invoice_key_date', frappe.datetime.get_today())
	},
	delete_bom(){
		frappe.confirm(__("This action will delete all the TSAI BOMs. It cannot be undone. Are you certain ?"), function() {
			frappe.call({
				method: "thaisummit.thaisummit.doctype.ekanban_settings.ekanban_settings.fetch_ekanban_bom",
				freeze: true,
				freeze_message: 'Updating....',
				callback(r) {
					if (r) {
						frappe.msgprint('BOM deleted successfully')
					}
				}
			})
		});
	},
	sync_grn(frm) {
		if (frm.doc.date) {
			frappe.call({
				method: "thaisummit.thaisummit.doctype.ekanban_settings.ekanban_settings.fetch_grn_details",
				args: {
					"date": frm.doc.date,
				},
				freeze: true,
				freeze_message: 'Updating....',
				callback(r) {
					if (r) {
						frappe.msgprint('GRN details updated successfully')
					}
				}
			})
		}
	},
	download(frm){
		// window.location.href = repl(frappe.request.url +
		// 	'?cmd=%(cmd)s', {
		// 	cmd: "thaisummit.thaisummit.doctype.ekanban_settings.ekanban_settings.enqueue_overall_invoice_key",
		// });
		frappe.call({
			method : "thaisummit.thaisummit.doctype.ekanban_settings.ekanban_settings.enqueue_overall_invoice_key"
		})
	},
	upolad(frm){
		frappe.confirm(__("This action will delete all the TSAI BOMs. It cannot be undone. Are you certain ?"), function() {
		console.log('hi');
	    frappe.call({
			method: "thaisummit.thaisummit.doctype.ekanban_settings.ekanban_settings.update_bom",
			args:{
				file : frm.doc.bob_file
			},
			freeze: true,
			freeze_message: 'Updating....',
			callback(r) {
				if (r) {
					frappe.msgprint('BOM deleted successfully and Upload Started')
				}
			}
		})
	});
	},
	download_invoice_key(frm){
		if (frm.doc.invoice_key_date) {
			// window.location.href = repl(frappe.request.url +
			// 	'?cmd=%(cmd)s&date=%(date)s', {
			// 	cmd: "thaisummit.thaisummit.doctype.ekanban_settings.ekanban_settings.enqueue_invoice_key_date_wise",
			// 	date: frm.doc.invoice_key_date
			// });
			frappe.call({
				method : "thaisummit.thaisummit.doctype.ekanban_settings.ekanban_settings.enqueue_invoice_key_date_wise",
				args : {
					invoice_key_date : frm.doc.invoice_key_date
				}
			})
		}
	}
});
