frappe.listview_settings["Tag Card"] = {
    onload: function(listview) {
        listview.filter_area.clear()
        listview.filter_area.add([["Tag Card", "docstatus", '=', 0]]);
        // fetch the production line value of the current user
        frappe.call({
            method: "thaisummit.thaisummit.doctype.tag_card.tag_card.update_list",
            callback: function(r) {
                if (r.message) {
                    listview.filter_area.add([[listview.doctype, "production_line", 'in', r.message]]);
                    listview.refresh();
                }
            }
        });

        frappe.call({
            method: "thaisummit.thaisummit.doctype.tag_card.tag_card.update_workflow_list",
            callback: function(r) {
                console.log(r)
                if (r.message) {
                    listview.filter_area.add([[listview.doctype, "allowed_role", 'in', r.message]]);
                    listview.refresh();
                }
            }
        });
    }
};