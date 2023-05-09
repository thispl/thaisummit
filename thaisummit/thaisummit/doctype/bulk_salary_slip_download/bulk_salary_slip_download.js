// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bulk Salary Slip Download', {
	refresh:function(frm){
		frm.disable_save()
		frm.refresh_field('salary_slip')
        frappe.breadcrumbs.add("Bulk Salary Slip Download");
		$('*[data-fieldname="salary_slip"]').find('.grid-remove-rows').hide();
		$('*[data-fieldname="salary_slip"]').find('.grid-remove-all-rows').hide();
		$('*[data-fieldname="salary_slip"]').find('.grid-add-row').remove()

		frm.fields_dict["salary_slip"].grid.add_custom_button(__('Download Salary Slip'),
			function () {
				$.each(frm.doc.salary_slip, function (i, d) {
					console.log(d.__checked);
					if (d.__checked == 1) {
						window.open(
							frappe.urllib.get_full_url(`/api/method/frappe.utils.print_format.download_pdf?
								doctype=${encodeURIComponent("Salary Slip")}
								&name=${encodeURIComponent(d.slip)}
								&format=${encodeURIComponent('Salary Slip New')}`)
						);
					}
				});
				
			}
		).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })
		// frm.add_custom_button('Download',function(){
		// 	var url = frappe.urllib.get_full_url(
		// 		'/api/method/thaisummit.thaisummit.doctype.bulk_salary_slip_download.bulk_salary_slip_download.get_pdf_link?'
		// 		)
		// 	$.ajax({
		// 		url: url,
		// 		type: 'GET',
		// 		success: function(result) {
		// 			if(jQuery.isEmptyObject(result)){
		// 				frappe.msgprint('No Records for these settings.');
		// 			}
		// 			else{
		// 				window.location = url;
		// 			}
		// 		}
		// 	});
		// });
	},
	// view_details(frm){
	// 	frappe.call({
	// 		method: "thaisummit.thaisummit.doctype.bulk_salary_slip_download.bulk_salary_slip_download.download_pdfs",
	// 		args: {
	// 			'start_date': frm.doc.start_date,
	// 			'employee_type': frm.doc.employee_type
	// 		},
	// 		callback: function(r){
	// 			if (r.message) {	
	// 				// $.each(r.message, function (i, v) {
	// 				// 	console.log(v)
	// 					// window.open(
	// 					// 	r.message);
						
	// 				// })	
	// 			}
	// 		}
    //     })
	// }
});
