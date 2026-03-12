frappe.listview_settings['Family Member'] = {
	refresh: function(listview) {
		// Check how many records have outdated ages
		frappe.call({
			method: "janadhikara.janadhikara.doctype.family_member.family_member.get_outdated_ages_count",
			callback: function(r) {
				if (r.message && r.message > 0) {
					// Add a custom button with the count of outdated records
					listview.page.add_inner_button(
						__("Update Ages ({0})", [r.message]),
						function() {
							frappe.call({
								method: "janadhikara.janadhikara.doctype.family_member.family_member.update_all_ages",
								freeze: true,
								freeze_message: __("Updating ages..."),
								callback: function(r2) {
									if (r2.message) {
										frappe.msgprint(
											__("{0} of {1} record(s) updated successfully.", 
											[r2.message.updated, r2.message.total])
										);
										listview.refresh();
									}
								}
							});
						}
					).addClass('btn-primary'); // Make the button visually stand out
				}
			}
		});
	}
};
