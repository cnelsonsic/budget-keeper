import unittest
from decimal import Decimal

from budgetkeeper.budgetkeeper import Account, MONTHLY

class TestAccount(unittest.TestCase):
    def test___init__(self):
        account = Account()
        self.assertEqual(len(account.transactions), 0)
        self.assertEqual(len(account.budgets), 0)

    def test_add_bill(self):
        account = Account()
        bill = account.add_bill(amount=100, description="Electricity", interval=MONTHLY)
        self.assertEqual(bill.amount, Decimal('100.00'))
        self.assertEqual(bill.description, 'Electricity')
        self.assertEqual(bill.interval, MONTHLY)
        self.assertIn(bill, account.transactions)

    def test_add_budget(self):
        # account = Account()
        # self.assertEqual(expected, account.add_budget(name, interval, limit, description))
        assert False # TODO: implement your test here

    def test_add_income(self):
        # account = Account()
        # self.assertEqual(expected, account.add_income(amount, description, timestamp, category))
        assert False # TODO: implement your test here

    def test_add_paycheck(self):
        # account = Account()
        # self.assertEqual(expected, account.add_paycheck(amount, description, timestamp, category, interval))
        assert False # TODO: implement your test here

    def test_add_purchase(self):
        # account = Account()
        # self.assertEqual(expected, account.add_purchase(amount, description, timestamp, category))
        assert False # TODO: implement your test here

    def test_balance(self):
        # account = Account()
        # self.assertEqual(expected, account.balance())
        assert False # TODO: implement your test here

    def test_get_budget_totals(self):
        # account = Account()
        # self.assertEqual(expected, account.get_budget_totals())
        assert False # TODO: implement your test here

    def test_parse_message(self):
        # account = Account()
        # self.assertEqual(expected, account.parse_message(message))
        assert False # TODO: implement your test here

    def test_trigger_recurring(self):
        # account = Account()
        # self.assertEqual(expected, account.trigger_recurring(timestamp))
        assert False # TODO: implement your test here


class TestTransaction(unittest.TestCase):
    def test___init__(self):
        # transaction = Transaction(amount, description, timestamp, category)
        assert False # TODO: implement your test here

class TestPayCheck(unittest.TestCase):
    def test___init__(self):
        # pay_check = PayCheck(amount, description, timestamp, category, interval)
        assert False # TODO: implement your test here

class TestBill(unittest.TestCase):
    def test___init__(self):
        # bill = Bill(amount, description, timestamp, category, interval)
        assert False # TODO: implement your test here

class TestBudget(unittest.TestCase):
    def test___init__(self):
        # budget = Budget(name, interval, limit, description)
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
