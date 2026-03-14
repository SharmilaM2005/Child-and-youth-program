# Copyright (c) 2026, TFSS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate
from datetime import date


class FamilyMember(Document):
    def validate(self):
        # 1. Update Age
        self.update_age()
        
        # 2. Update Category based on Age (Calls utility function below)
        self.child_youth = determine_child_youth(self.age)
        
        # 3. Update Enrollment Status
        self.update_program_status()

    def update_age(self):
        """Update age based on date_of_birth"""
        if self.date_of_birth:
            self.age = calculate_age(self.date_of_birth)

    def update_program_status(self):
        """Update program status based on age category and enrollment"""

        if not self.name:
            self.program_status = "Not Eligible"
            return

        # CHILD PROGRAM
        if self.child_youth == "Child":

            clc_enrolled = frappe.db.exists(
                "CLC Enrollment",
                {"fmid": self.name}
            )

            if clc_enrolled:
                self.program_status = "CLC Enrolled"
            else:
                self.program_status = "CLC Not Enrolled"

            return


        # YOUTH PROGRAM
        if self.child_youth == "Youth":

            ylc_enrolled = frappe.db.exists(
                "YLC Enrollment",
                {"fmid": self.name}
            )

            if ylc_enrolled:
                self.program_status = "YLC Enrolled"
            else:
                self.program_status = "YLC Not Enrolled"

            return


        # NOT ELIGIBLE
        self.program_status = "Not Eligible"


# ---------------- Utility Functions ----------------
# These must be OUTSIDE the class so tasks.py can import them directly.

def determine_child_youth(age):
    """
    Python version of JS update_age_and_category.
    Fetches rules from 'Age Category' doctype.
    """
    if age is None or age == "":
        return ""
    
    # Fetch categories from the database
    categories = frappe.get_all("Age Category", fields=["category_name", "min_age", "max_age"])
    
    for row in categories:
        if age >= row.min_age and age <= row.max_age:
            return row.category_name
            
    return ""


def calculate_age(date_of_birth):
    """Calculates age from date of birth"""
    if not date_of_birth:
        return 0
    dob = getdate(date_of_birth)
    today = date.today()
    age = today.year - dob.year
    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1
    return age


def update_family_member_ages():
    """
    Triggered by hooks/scheduler. 
    Updates all members to ensure age/category is current.
    """
    members = frappe.get_all("Family Member", fields=["name"])
    for member in members:
        try:
            doc = frappe.get_doc("Family Member", member.name)
            doc.save() # This triggers the validate() logic above
        except Exception:
            pass