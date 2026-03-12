# Copyright (c) 2026, TFSS and contributors
# For license information, please see license.txt

import frappe
from janadhikara.janadhikara.doctype.family_member.family_member import calculate_age, determine_child_youth


def update_family_member_ages():
	"""Daily scheduled task to recalculate age and child/youth category for all Family Members."""
	family_members = frappe.get_all(
		"Family Member",
		filters={"date_of_birth": ["is", "set"]},
		fields=["name", "date_of_birth", "age", "child_youth"],
	)

	for member in family_members:
		new_age = calculate_age(member.date_of_birth)
		new_child_youth = determine_child_youth(new_age)
		
		updates = {}
		if str(new_age) != str(member.age):
			updates["age"] = new_age
		if new_child_youth != member.child_youth:
			updates["child_youth"] = new_child_youth
			
		if updates:
			frappe.db.set_value("Family Member", member.name, updates, update_modified=False)

	frappe.db.commit()
