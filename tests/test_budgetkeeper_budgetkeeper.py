import unittest
from decimal import Decimal

from datetime import datetime

from budgetkeeper.budgetkeeper import Account, MONTHLY

class TestAccount(unittest.TestCase):
    def test___init__(self):
        account = Account()
        self.assertEqual(len(account.transactions), 0)
        self.assertEqual(len(account.budgets), 0)

    def test_add_bill(self):
        account = Account()
        bill = account.add_bill(amount=100, description="Electricity", interval=MONTHLY)
        self.assertIn(bill, account.transactions)
        self.assertEqual(bill.amount, Decimal('100.00'))
        self.assertEqual(bill.description, 'Electricity')
        self.assertEqual(bill.interval, MONTHLY)

    def test_add_budget(self):
        account = Account()
        budget = account.add_budget(name='Test Budget', interval=MONTHLY, limit=1000)
        self.assertIn(budget, account.budgets)
        self.assertEqual(budget.name, 'Test Budget')
        self.assertEqual(budget.interval, MONTHLY)
        self.assertEqual(budget.limit, Decimal('1000.00'))

    def test_add_income(self):
        account = Account()
        income = account.add_income(amount=1000, description="Gift", timestamp=datetime(2012, 1, 1))
        self.assertIn(income, account.transactions)
        self.assertEqual(income.amount, Decimal('1000.00'))
        self.assertEqual(income.description, 'Gift')
        self.assertEqual(income.timestamp, datetime(2012, 1, 1))

    def test_add_paycheck(self):
        # account = Account()
        # self.assertEqual(expected, account.add_paycheck(amount, description, timestamp, category, interval))
        assert False # TODO: implement your test here

    def test_add_purchase(self):
        # account = Account()
        # self.assertEqual(expected, account.add_purchase(amount, description, timestamp, category))
        assert False # TODO: implement your test here

    def test_balance(self):
        account = Account()
        account.add_income(amount=100)
        result = account.balance
        expected = Decimal(100)
        self.assertEqual(expected, result)

    def test_get_budget_totals(self):
        account = Account()
        account.add_budget('Groceries', interval=MONTHLY, limit=1000)
        account.add_purchase(100, category='Groceries')

        result = account.get_budget_totals()
        expected = {'Groceries': Decimal(100)}
        self.assertEqual(result, expected)

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
