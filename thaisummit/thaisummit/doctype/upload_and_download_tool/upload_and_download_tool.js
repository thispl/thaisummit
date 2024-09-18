// Copyright (c) 2023, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Upload and Download Tool', {
	download_pcs_part_master: function (frm) {
		window.location.href = repl(frappe.request.url +
			'?cmd=%(cmd)s', {
			cmd: "thaisummit.thaisummit.doctype.upload_and_download_tool.upload_and_download_tool.download_pcs_part_master",
		});
	},
	download_templete_for_pcs_part_master:function (frm){
		window.location.href = repl(frappe.request.url +
			'?cmd=%(cmd)s', {
			cmd: "thaisummit.thaisummit.doctype.upload_and_download_tool.upload_and_download_tool.download_template_pcs_part_master",
		});
	},
	download_scrap_master:function(frm){
		window.location.href = repl(frappe.request.url +
			'?cmd=%(cmd)s', {
			cmd: "thaisummit.thaisummit.doctype.upload_and_download_tool.upload_and_download_tool.download_pcs_scrap_master",
		});
	},
	download_templete_for_pcs_scrap_master:function(frm){
		window.location.href = repl(frappe.request.url +
			'?cmd=%(cmd)s', {
			cmd: "thaisummit.thaisummit.doctype.upload_and_download_tool.upload_and_download_tool.download_template_pcs_scrap_master",
		});
	},
	upload_scrap_master:function(frm){
		frappe.call({
			method: "thaisummit.thaisummit.doctype.upload_and_download_tool.upload_and_download_tool.enqueue_scrap_master",
			args:{
				file : frm.doc.attach_scrap_master
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
	upload_pcs_part_master:function(frm){
		frappe.call({
			method: "thaisummit.thaisummit.doctype.upload_and_download_tool.upload_and_download_tool.enqueue_pcs_part_master",
			args:{
				attach_file : frm.doc.attach_pcs_part_master
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
