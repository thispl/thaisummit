frappe.listview_settings['Shift Schedule'] = {
    onload(listview) {
		frappe.breadcrumbs.add('Shift Schedule','Home');
	listview.page.actions.find('[data-label="Edit"],[data-label="Assign To"],[data-label="Apply Assignment Rule"],[data-label="Add Tags"],[data-label="Print"]').parent().parent().remove()
	listview.page.fields_dict.workflow_state.get_query = function() {
		return {
			"filters": {
				"name": ["in", ["Pending for HOD","Pending for GM","Approved","Rejected"]],
			}
		};
	};
	},
};
