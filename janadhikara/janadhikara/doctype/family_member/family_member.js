frappe.ui.form.on("Family Member", {

	refresh(frm) {
		if (frm.doc.date_of_birth) {
			update_age_and_category(frm);
		}
	},

	date_of_birth(frm) {
		if (frm.doc.date_of_birth) {
			update_age_and_category(frm);
		} else {
			frm.set_value("age", "");
			frm.set_value("child_youth", "");
		}
	}

});


function update_age_and_category(frm) {

	let age = calculate_age(frm.doc.date_of_birth);
	frm.set_value("age", age);

	frappe.db.get_list("Age Category", {
		fields: ["category_name", "min_age", "max_age"]
	}).then(records => {

		let category = "";

		records.forEach(row => {

			if (age >= row.min_age && age <= row.max_age) {
				category = row.category_name;
			}

		});

		frm.set_value("child_youth", category);

	});

}


function calculate_age(date_of_birth) {

	let dob = frappe.datetime.str_to_obj(date_of_birth);
	let today = frappe.datetime.str_to_obj(frappe.datetime.get_today());

	let age = today.getFullYear() - dob.getFullYear();
	let month_diff = today.getMonth() - dob.getMonth();

	if (month_diff < 0 || (month_diff === 0 && today.getDate() < dob.getDate())) {
		age--;
	}

	return age;

}