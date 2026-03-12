# Copyright (c) 2026, TFSS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today


class FamilyMember(Document):
	def validate(self):
		if self.date_of_birth:
			self.age = calculate_age(self.date_of_birth)
			self.child_youth = determine_child_youth(self.age)


def calculate_age(date_of_birth):
	"""Calculate age in years from date of birth."""
	dob = getdate(date_of_birth)
	current_date = getdate(today())

	age = current_date.year - dob.year

	# If birthday hasn't occurred yet this year, subtract 1
	if (current_date.month, current_date.day) < (dob.month, dob.day):
		age -= 1

	return age


def determine_child_youth(age):
	"""Determine if the age falls under Child or Youth category."""
	if 4 <= age <= 14:
		return "Child"
	elif 15 <= age <= 26:
		return "Youth"
	return ""

@frappe.whitelist()
def get_outdated_ages_count():
	family_members = frappe.get_all(
		"Family Member",
		filters={"date_of_birth": ["is", "set"]},
		fields=["name", "date_of_birth", "age", "child_youth"],
	)
	outdated_count = 0
	for member in family_members:
		new_age = calculate_age(member.date_of_birth)
		new_child_youth = determine_child_youth(new_age)
		if str(new_age) != str(member.age) or str(new_child_youth) != str(member.child_youth):
			outdated_count += 1
	return outdated_count

@frappe.whitelist()
def update_all_ages():
	family_members = frappe.get_all(
		"Family Member",
		filters={"date_of_birth": ["is", "set"]},
		fields=["name", "date_of_birth", "age", "child_youth"],
	)
	updated_count = 0
	total_records = len(family_members)
	for member in family_members:
		new_age = calculate_age(member.date_of_birth)
		new_child_youth = determine_child_youth(new_age)
		
		updates = {}
		if str(new_age) != str(member.age):
			updates["age"] = new_age
		if str(new_child_youth) != str(member.child_youth):
			updates["child_youth"] = new_child_youth
			
		if updates:
			frappe.db.set_value("Family Member", member.name, updates, update_modified=False)
			updated_count += 1
			
	if updated_count > 0:
		frappe.db.commit()
		
	return {"updated": updated_count, "total": total_records}
