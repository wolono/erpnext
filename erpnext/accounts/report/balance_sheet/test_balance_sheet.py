# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

import frappe
<<<<<<< HEAD
from frappe.tests.utils import FrappeTestCase
from frappe.utils import today

from erpnext.accounts.report.balance_sheet.balance_sheet import execute


class TestBalanceSheet(FrappeTestCase):
	def test_balance_sheet(self):
		from erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice import make_purchase_invoice
		from erpnext.accounts.doctype.sales_invoice.test_sales_invoice import (
			create_sales_invoice,
		)

		frappe.db.sql("delete from `tabPurchase Invoice` where company='_Test Company 6'")
		frappe.db.sql("delete from `tabSales Invoice` where company='_Test Company 6'")
		frappe.db.sql("delete from `tabGL Entry` where company='_Test Company 6'")

		make_purchase_invoice(
			company="_Test Company 6",
			warehouse="Finished Goods - _TC6",
			expense_account="Cost of Goods Sold - _TC6",
			cost_center="Main - _TC6",
			qty=10,
			rate=100,
		)
		create_sales_invoice(
			company="_Test Company 6",
			debit_to="Debtors - _TC6",
			income_account="Sales - _TC6",
			cost_center="Main - _TC6",
			qty=5,
			rate=110,
		)
		filters = frappe._dict(
			company="_Test Company 6",
=======
from frappe.tests import IntegrationTestCase
from frappe.utils.data import today

from erpnext.accounts.report.balance_sheet.balance_sheet import execute

COMPANY = "_Test Company 6"
COMPANY_SHORT_NAME = "_TC6"

EXTRA_TEST_RECORD_DEPENDENCIES = ["Company"]


class TestBalanceSheet(IntegrationTestCase):
	def test_balance_sheet(self):
		frappe.db.sql(f"delete from `tabJournal Entry` where company='{COMPANY}'")
		frappe.db.sql(f"delete from `tabGL Entry` where company='{COMPANY}'")

		create_account("VAT Liabilities", f"Duties and Taxes - {COMPANY_SHORT_NAME}", COMPANY)
		create_account("Advance VAT Paid", f"Duties and Taxes - {COMPANY_SHORT_NAME}", COMPANY)
		create_account("My Bank", f"Bank Accounts - {COMPANY_SHORT_NAME}", COMPANY)

		# 1000 equity paid to bank account
		make_journal_entry(
			[
				dict(
					account_name="My Bank",
					debit_in_account_currency=1000,
					credit_in_account_currency=0,
				),
				dict(
					account_name="Capital Stock",
					debit_in_account_currency=0,
					credit_in_account_currency=1000,
				),
			]
		)

		# 110 income paid to bank account (100 revenue + 10 VAT)
		make_journal_entry(
			[
				dict(
					account_name="My Bank",
					debit_in_account_currency=110,
					credit_in_account_currency=0,
				),
				dict(
					account_name="Sales",
					debit_in_account_currency=0,
					credit_in_account_currency=100,
				),
				dict(
					account_name="VAT Liabilities",
					debit_in_account_currency=0,
					credit_in_account_currency=10,
				),
			]
		)

		# offset VAT Liabilities with intra-year advance payment
		make_journal_entry(
			[
				dict(
					account_name="My Bank",
					debit_in_account_currency=0,
					credit_in_account_currency=10,
				),
				dict(
					account_name="Advance VAT Paid",
					debit_in_account_currency=10,
					credit_in_account_currency=0,
				),
			]
		)

		filters = frappe._dict(
			company=COMPANY,
>>>>>>> 325b20491a (fix: make rate of depreciation mandatory)
			period_start_date=today(),
			period_end_date=today(),
			periodicity="Yearly",
		)
<<<<<<< HEAD
		result = execute(filters)[1]
		for account_dict in result:
			if account_dict.get("account") == "Current Liabilities - _TC6":
				self.assertEqual(account_dict.total, 1000)
			if account_dict.get("account") == "Current Assets - _TC6":
				self.assertEqual(account_dict.total, 550)
=======
		results = execute(filters)
		name_and_total = {
			account_dict["account_name"]: account_dict["total"]
			for account_dict in results[1]
			if "total" in account_dict and "account_name" in account_dict
		}

		self.assertNotIn("Sales", name_and_total)

		self.assertIn("My Bank", name_and_total)
		self.assertEqual(name_and_total["My Bank"], 1100)

		self.assertIn("VAT Liabilities", name_and_total)
		self.assertEqual(name_and_total["VAT Liabilities"], 10)

		self.assertIn("Advance VAT Paid", name_and_total)
		self.assertEqual(name_and_total["Advance VAT Paid"], -10)

		self.assertIn("Duties and Taxes", name_and_total)
		self.assertEqual(name_and_total["Duties and Taxes"], 0)

		self.assertIn("Application of Funds (Assets)", name_and_total)
		self.assertEqual(name_and_total["Application of Funds (Assets)"], 1100)

		self.assertIn("Equity", name_and_total)
		self.assertEqual(name_and_total["Equity"], 1000)

		self.assertIn("'Provisional Profit / Loss (Credit)'", name_and_total)
		self.assertEqual(name_and_total["'Provisional Profit / Loss (Credit)'"], 100)


def make_journal_entry(rows):
	jv = frappe.new_doc("Journal Entry")
	jv.posting_date = today()
	jv.company = COMPANY
	jv.user_remark = "test"

	for row in rows:
		row["account"] = row.pop("account_name") + " - " + COMPANY_SHORT_NAME
		jv.append("accounts", row)

	jv.insert()
	jv.submit()


def create_account(account_name: str, parent_account: str, company: str):
	if frappe.db.exists("Account", {"account_name": account_name, "company": company}):
		return

	acc = frappe.new_doc("Account")
	acc.account_name = account_name
	acc.company = COMPANY
	acc.parent_account = parent_account
	acc.insert()
>>>>>>> 325b20491a (fix: make rate of depreciation mandatory)
