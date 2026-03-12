// Copyright (c) 2026, TFSS and contributors
// For license information, please see license.txt

frappe.ui.form.on("Family Member", {
	refresh(frm) {
		// Recalculate age on form refresh (in case birthday has passed since last save)
		if (frm.doc.date_of_birth) {
			let age = calculate_age(frm.doc.date_of_birth);
			frm.set_value("age", age);
			frm.set_value("child_youth", determine_child_youth(age));
		}
	},

	date_of_birth(frm) {
		if (frm.doc.date_of_birth) {
			let age = calculate_age(frm.doc.date_of_birth);
			frm.set_value("age", age);
			frm.set_value("child_youth", determine_child_youth(age));
		} else {
			frm.set_value("age", "");
			frm.set_value("child_youth", "");
		}
	},
});

function calculate_age(date_of_birth) {
	let dob = frappe.datetime.str_to_obj(date_of_birth);
	let today = frappe.datetime.str_to_obj(frappe.datetime.get_today());

	let age = today.getFullYear() - dob.getFullYear();
	let month_diff = today.getMonth() - dob.getMonth();

	// If birthday hasn't occurred yet this year, subtract 1
	if (month_diff < 0 || (month_diff === 0 && today.getDate() < dob.getDate())) {
		age--;
	}

	return age;
}

function determine_child_youth(age) {
	if (age >= 4 && age <= 14) {
		return "Child";
	} else if (age >= 15 && age <= 26) {
		return "Youth";
	}
	return "";
}
