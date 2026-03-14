# # Copyright (c) 2026, TFSS and contributors
# # For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate	
from datetime import date


class FamilyMember(Document):

	def validate(self):
		self.update_age()
		self.update_child_youth()
		self.update_program_status()


	def update_age(self):
		"""Update age based on date_of_birth"""
		if self.date_of_birth:
			self.age = calculate_age(self.date_of_birth)


	def update_child_youth(self):
		"""Determine if member is Child or Youth"""
		if self.age is not None:
			self.child_youth = determine_child_youth(self.age)


	def update_program_status(self):
		"""Update program status based on enrollment"""

		status = "Not Eligible"

		if not self.name:
			self.program_status = status
			return

		# Youth → Check YLC Enrollment
		if self.child_youth == "Youth":

			enrolled = frappe.db.exists(
				"YLC Enrollment",   # ← correct name
				{"fmid": self.name}
			)

			status = "YLC Enrolled" if enrolled else "YLC Not Enrolled"

		# Child → Check CLC Enrollment
		elif self.child_youth == "Child":

			enrolled = frappe.db.exists(
				"CLC Enrollment",   # ← correct name
				{"fmid": self.name}
			)

			status = "CLC Enrolled" if enrolled else "CLC Not Enrolled"

		self.program_status = status


# ---------------- Utility Functions ----------------

def calculate_age(date_of_birth):

    dob = getdate(date_of_birth)
    today = date.today()

    age = today.year - dob.year

    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1

    return age


def determine_child_youth(age):
	"""Return Child or Youth based on age"""

	if 4 <= age <= 14:
		return "Child"

	elif 15 <= age <= 26:
		return "Youth"

	return ""

