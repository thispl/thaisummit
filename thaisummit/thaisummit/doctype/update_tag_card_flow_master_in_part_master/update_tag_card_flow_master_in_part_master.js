// Copyright (c) 2023, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Update Tag Card Flow Master in Part Master', {
	download_template:function(frm){
		console.log('hi')
		window.location.href = repl(frappe.request.url +
			'?cmd=%(cmd)s', {
			cmd: "thaisummit.thaisummit.doctype.update_tag_card_flow_master_in_part_master.update_tag_card_flow_master_in_part_master.download_template",
		});
	},
	upload:function(frm){
		frappe.call({
			method: "thaisummit.thaisummit.doctype.update_tag_card_flow_master_in_part_master.update_tag_card_flow_master_in_part_master.enqueue_tag_card_flow_upload",
			args:{
				file : frm.doc.attach_file_here
			},
			freeze: true,
			freeze_message: 'Updating....',
			callback(r) {
				if (r) {
					frappe.msgprint('Upload Started in background')
				}
			}
		})

	},
	refresh: function(frm) {
		frm.disable_save()
	}
});
