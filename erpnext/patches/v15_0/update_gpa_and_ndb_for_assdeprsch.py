import frappe


def execute():
	# not using frappe.qb because https://github.com/frappe/frappe/issues/20292
<<<<<<< HEAD
	# nosemgrep
=======
>>>>>>> 325b20491a (fix: make rate of depreciation mandatory)
	frappe.db.sql(
		"""UPDATE `tabAsset Depreciation Schedule`
        JOIN `tabAsset`
        ON `tabAsset Depreciation Schedule`.`asset`=`tabAsset`.`name`
        SET
            `tabAsset Depreciation Schedule`.`gross_purchase_amount`=`tabAsset`.`gross_purchase_amount`,
            `tabAsset Depreciation Schedule`.`opening_number_of_booked_depreciations`=`tabAsset`.`opening_number_of_booked_depreciations`
        WHERE
        (
            `tabAsset Depreciation Schedule`.`gross_purchase_amount`<>`tabAsset`.`gross_purchase_amount`
            OR
            `tabAsset Depreciation Schedule`.`opening_number_of_booked_depreciations`<>`tabAsset`.`opening_number_of_booked_depreciations`
        )
        AND `tabAsset Depreciation Schedule`.`docstatus`<2"""
	)
