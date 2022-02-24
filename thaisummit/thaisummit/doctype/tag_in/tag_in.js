// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('TAG IN', {
    submit: function (frm) {
        cur_frm.set_df_property("submit", "hidden", true);
        var today = new Date();

        var date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();

        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        var datetime = date + ' ' + time
        frm.set_value("submit_time", datetime)
        frm.call('new_tag_slot')
            .then(r => {
                var message = "TAG Slot No - {" + r.message + "} Created"
                frappe.show_alert(__(message), 5);
                frappe.set_route('Form','Tag Slot', r.message);
            })
    },
    refresh: function (frm) {
        frm.disable_save()
        $("input[data-fieldname='vehicle']").focus()

    },

    qr: function (frm) {
        var today = new Date();
        var date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        var datetime = date + ' ' + time
        var qr_length = (frm.doc.qr).length
        if (qr_length == 68) {
            var part_no = frm.doc.qr.substring(11, 25)
            var qty = frm.doc.qr.substring(38, 43)

            frappe.db.get_doc('Part Master', null,{'parts_no':part_no})
                .then(doc => {
                    frm.add_child("receipt_entry_table", {
                        vehicle : frm.doc.vehicle,
                        model_number: frm.doc.model_number,
                        parts_no: doc.name,
                        quantity: parseInt(qty, 10),
                        card_type: doc.tag_type,
                        parts_name: doc.parts_name,
                        mat_no: doc.mat_no,
                        model: doc.model_no,
                        date_and_time: datetime,
                        qr: frm.doc.qr
                    })
                    frm.set_value("qr", "");
                    frm.refresh_field("receipt_entry_table")
                })
        }
        else if (qr_length == 49) {
            console.log(qr_length)
            var part_no = frm.doc.qr.substring(11, 25)
            var qty = frm.doc.qr.substring(44, 49)
            frappe.db.get_doc('Part Master',null, {'parts_no':part_no})
                .then(doc => {
                    frm.add_child("receipt_entry_table", {
                        vehicle : frm.doc.vehicle,
                        model_number: frm.doc.model_number,
                        parts_no: doc.name,
                        quantity: parseInt(qty, 10),
                        card_type: doc.tag_type,
                        parts_name: doc.parts_name,
                        mat_no: doc.mat_no,
                        model: doc.model_no,
                        date_and_time: datetime,
                        qr: frm.doc.qr
                    });
                    frm.set_value("qr", "");
                    frm.refresh_field("receipt_entry_table")
                })
        }
        // else{
        //     frappe.msgprint(__('Invalid QR Digit Length; Kindly check the QR entered or update the system with new QR'));
        // }
        
    }
});
