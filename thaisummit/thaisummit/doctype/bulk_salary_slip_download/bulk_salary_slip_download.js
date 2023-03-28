// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bulk Salary Slip Download', {
	refresh:function(frm){
		frm.add_custom_button('Download',function(){
			var url = frappe.urllib.get_full_url(
				'/api/method/thaisummit.thaisummit.doctype.bulk_salary_slip_download.bulk_salary_slip_download.get_pdf_link?'
				)
			$.ajax({
				url: url,
				type: 'GET',
				success: function(result) {
					if(jQuery.isEmptyObject(result)){
						frappe.msgprint('No Records for these settings.');
					}
					else{
						window.location = url;
					}
				}
			});
		});
	},
	download_slip(frm){
		frappe.call({
			method: "thaisummit.thaisummit.doctype.bulk_salary_slip_download.bulk_salary_slip_download.get_pdf_link",
			args: {
			},
			callback: function(r)
			{
				console.log(r)
				if (r.message) {
					
					// $.each(r.message, function (i, v) {
					// 	frm.add_child('salary_slip',{
					// 		'slip':v.name
					// 	})
					// 	frm.refresh_field('salary_slip')
					// })
					// window.open(
					// 		frappe.urllib.get_full_url(`/api/method/frappe.utils.print_format.download_multi_pdf?
					// 		doctype=${encodeURIComponent("Salary Slip")}
					// 		&name=${encodeURIComponent(v.name)}
					// 		&format=${encodeURIComponent('Salary Slip New')}`)
					// );	
				}
			}
        })
	}
});
