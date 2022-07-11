// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Food Entry Scan', {
	
	
	employee_guest(frm){
		if(frm.doc.employee_guest){
			frappe.call({
				method:'thaisummit.thaisummit.doctype.food_entry_scan.food_entry_scan.get_canteen_user_id',
				args:{
					user:frm.doc.employee_guest,
					cur_date:frm.doc.date
				},
				callback(r){
					console.log(r.message)
					if(r.message == 'Completed'){
						frm.set_value('employee_guest','')
						frm.trigger('get_live_screen')
					}
					// else{
					// 	// frm.set_value('employee_guest','')	
					// 	frm.trigger('get_live_screen')
					// }
					
					// setTimeout(function(){
						
					// 	frm.get_field("output").$wrapper.html('');
					//  }, 5000);
				}
			})
		}
		
	},
	get_live_screen(frm){
		frappe.call({
			method:'thaisummit.www.canteen_live_screen.get_live_screen_data',
			args:{
			},
			callback(r){
				var data = r.message;
			var html = `<table border="1px solid" width="100%">
				<tr>\
					<td colspan="7"  style="background-color:#90ee90">
						<center>\
							<h3 style="color:#000000"><b>${data["current_datetime"]}</b></h3>\
						</center>\
					</td>\
				</tr>\
			</table> `
				frm.fields_dict.output.$wrapper.empty().append(frappe.render_template('canteen_live_screen_data',r.message))
				// frm.fields_dict.output.$wrapper.empty().append(html)
			
			}
			
		})
	},
	refresh(frm){
		frm.disable_save()
		frm.trigger("get_live_screen")
	}
});
