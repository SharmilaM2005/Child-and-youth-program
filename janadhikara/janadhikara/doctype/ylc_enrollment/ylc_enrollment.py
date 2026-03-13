# Copyright (c) 2026, TFSS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class YLCEnrollment(Document):

    def validate(self):
        self.prevent_duplicate_enrollment()

    def after_insert(self):
        self.update_family_member_status()

    def on_update(self):
        self.update_family_member_status()

    def on_trash(self):
        self.update_family_member_status()


    def prevent_duplicate_enrollment(self):
        """Prevent same Family Member from enrolling twice in YLC"""

        if not self.fmid:
            return

        existing = frappe.get_all(
            "YLC Enrollment",
            filters={
                "fmid": self.fmid,
                "name": ["!=", self.name]
            },
            limit=1
        )

        if existing:
            frappe.throw("This Family Member is already enrolled in YLC.")


    def update_family_member_status(self):
        """Trigger Family Member to recalculate program status"""

        if not self.fmid:
            return

        member = frappe.get_doc("Family Member", self.fmid)
        member.save(ignore_permissions=True)