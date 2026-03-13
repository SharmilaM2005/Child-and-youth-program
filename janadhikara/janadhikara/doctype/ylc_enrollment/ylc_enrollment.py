import frappe
from frappe.model.document import Document


class YLCEnrollment(Document):

    def validate(self):
        self.prevent_duplicate_enrollment()

    def after_insert(self):
        self.update_family_member_status()

    def on_trash(self):
        self.update_family_member_status()

    def prevent_duplicate_enrollment(self):

        if not self.fmid:
            return

        existing = frappe.db.exists(
            "YLC Enrollment",
            {
                "fmid": self.fmid,
                "name": ["!=", self.name]
            }
        )

        if existing:
            frappe.throw("This Family Member is already enrolled in YLC.")

    def update_family_member_status(self):

        if not self.fmid:
            return

        member = frappe.get_doc("Family Member", self.fmid)
        member.save(ignore_permissions=True)