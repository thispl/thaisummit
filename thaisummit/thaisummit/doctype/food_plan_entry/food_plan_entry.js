// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Food Plan Entry', {
	refresh(frm){
		frm.fields_dict['food_plan_child'].grid.wrapper.find('.grid-add-row').remove();
		frm.fields_dict['food_plan_child'].grid.wrapper.find('.grid-remove-rows').remove();
		frm.fields_dict['food_plan_child'].grid.wrapper.find('.edit-grid-row').hide();
		$('*[data-fieldname="food_plan_child"]').find('.grid-remove-all-rows').hide();

	},
	setup(frm){
		frm.get_docfield('food_plan_child').allow_bulk_edit = 1
	},
	onload(frm) {
		frm.set_value('date',frappe.datetime.nowdate())
		frm.trigger("validate_dates")
		frm.trigger("get_food_plan")
		frm.disable_save()
		// $('.edit-grid-row').hide()
	},
	validate_dates(frm){
		var current_date = frappe.datetime.nowdate()
		if (frm.doc.date < current_date){
			frm.set_read_only()
		}
	},
	date(frm) {
		frm.trigger("get_food_plan")
		frm.trigger("validate_dates")
	},
	get_food_plan(frm) {
		frm.set_value("food_plan_child", [])
		frappe.call({
			method: "thaisummit.thaisummit.doctype.food_plan_entry.food_plan_entry.get_food_plan",
			args: {
				"date": frm.doc.date
			},
			callback(r) {
				frm.set_value("food_plan_child", [])
				
				if (r.message && r.message.length == 0) {
					frappe.call({
						method: "frappe.client.get_list",
						args: {
							"doctype": "Food Menu",
							'fields': ["name",'price'],
							"order_by": "priority",
						},
						
						callback(r) {
							if (r.message) {
								$.each(r.message, function (i, v) {
									frm.add_child("food_plan_child", {
										"menu": v['name'],
										"price":v['price']
									})
								});
								frm.refresh_field("food_plan_child")
							}
						}
					})
				}
				else {
					$.each(r.message, function (i, v) {
						frm.add_child("food_plan_child", {
							"menu": "Break Fast",
							"head_count": v['bf_head_count'],
							"price": v['bf_price'],
							"amount": v['bf_amount']
						}),
						frm.add_child("food_plan_child", {
							"menu": "Lunch",
							"head_count": v['lu_head_count'],
							"price": v['lu_price'],
							"amount": v['lu_amount']
						}),
						frm.add_child("food_plan_child", {
							"menu": "Lunch Briyani Veg",
							"head_count": v['lbv_head_count'],
							"price": v['lbv_price'],
							"amount": v['lbv_amount']
						}),
						frm.add_child("food_plan_child", {
							"menu": "Lunch Briyani Non Veg",
							"head_count": v['lbnv_head_count'],
							"price": v['lbnv_price'],
							"amount": v['lbnv_amount']
						}),
						frm.add_child("food_plan_child", {
							"menu": "Lunch Special Veg",
							"head_count": v['lsv_head_count'],
							"price": v['lsv_price'],
							"amount": v['lsv_amount']
						}),
						frm.add_child("food_plan_child", {
							"menu": "Lunch Special Non Veg",
							"head_count": v['lsnv_head_count'],
							"price": v['lsnv_price'],
							"amount": v['lsnv_amount']
						}),
						frm.add_child("food_plan_child", {
							"menu": "Dinner",
							"head_count": v['dn_head_count'],
							"price": v['dn_price'],
							"amount": v['dn_amount']
						}),
						frm.add_child("food_plan_child", {
							"menu": "Dinner Briyani Veg",
							"head_count": v['dbv_head_count'],
							"price": v['dbv_price'],
							"amount": v['dbv_amount']
						}),
						frm.add_child("food_plan_child", {
							"menu": "Dinner Briyani Non Veg",
							"head_count": v['dbnv_head_count'],
							"price": v['dbnv_price'],
							"amount": v['dbnv_amount']
						}),
						frm.add_child("food_plan_child", {
							"menu": "Dinner Special Veg",
							"head_count": v['dsv_head_count'],
							"price": v['dsv_price'],
							"amount": v['dsv_amount']
						}),
						frm.add_child("food_plan_child", {
							"menu": "Dinner Special Non Veg",
							"head_count": v['dsnv_head_count'],
							"price": v['dsnv_price'],
							"amount": v['dsnv_amount']
						}),
						frm.add_child("food_plan_child", {
							"menu": "Supper",
							"head_count": v['sp_head_count'],
							"price": v['sp_price'],
							"amount": v['sp_amount']
						}),
						frm.add_child("food_plan_child", {
							"menu": "Supper Dates",
							"head_count": v['sd_head_count'],
							"price": v['sd_price'],
							"amount": v['sd_amount']
						}),
						frm.add_child("food_plan_child", {
							"menu": "Supper Special Food",
							"head_count": v['ssf_head_count'],
							"price": v['ssf_price'],
							"amount": v['ssf_amount']
						})
						

					})
					frm.refresh_field("food_plan_child")
				}
			}
		})
	},
	update(frm) {
		frappe.call({
			method: "thaisummit.thaisummit.doctype.food_plan_entry.food_plan_entry.update_food_plan",
			args: {
				"food_plan_child": frm.doc.food_plan_child,
				"date": frm.doc.date
			},
			callback(r) {
				frappe.msgprint('Updated')
			}
		})
	}

});
frappe.ui.form.on('Food Plan Child', {
	head_count(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		row.amount = row.head_count * row.price
		frm.refresh_field("food_plan_child");

	},
	price(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		row.amount = row.head_count * row.price
		frm.refresh_field("food_plan_child");
	}
});
