frappe.listview_settings["Generate Tag Card"] = {
    onload: function(listview) {
        // fetch the production line value of the current user
        frappe.call({
            method: "thaisummit.thaisummit.doctype.tag_card.tag_card.update_list",
            callback: function(r) {
                if (r.message) {
                    console.log(r)
                    listview.filter_area.clear()
                    listview.filter_area.add([[listview.doctype, "production_line", 'in', r.message]]);
                    listview.refresh();
                }
            }
        });

    }
}