import unittest
from decimal import Decimal

from datetime import datetime

from budgetkeeper.budgetkeeper import Account, Message, MONTHLY

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
        account = Account()
        paycheck = account.add_paycheck(1000, description="Paycheck from WebApps Inc.", interval=MONTHLY)
        self.assertIn(paycheck, account.transactions)
        self.assertEqual(paycheck.amount, Decimal('1000.00'))
        self.assertIn('WebApps Inc.', paycheck.description)
        self.assertEqual(paycheck.interval, MONTHLY)

    def test_add_purchase(self):
        account = Account()
        purchase = account.add_purchase(1000, description="Morning Coffee")
        self.assertIn(purchase, account.transactions)
        self.assertEqual(purchase.amount, Decimal('1000.00'))
        self.assertEqual('Morning Coffee', purchase.description)

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
        self.skip("TODO: Not Implemented")

    def test_trigger_recurring(self):
        # account = Account()
        # self.assertEqual(expected, account.trigger_recurring(timestamp))
        self.skip("TODO: Not Implemented")

class TestMessage(unittest.TestCase):

    def test_get_money(self):
        test_data = (('$4.12', '4.12'),
                     ('4.12', '4.12'),
                     ('.12', '.12'),
                     ('Paid $4.12 for a latte.', '4.12'),
                     ('Paid $14.57 for a book from the used bookstore.', '14.57'),
                     ('Bought a new pair of pants for $5. Quite a steal.', '5'),
                     ("[18:34] <joe> I bought a new widget today, was only $0.99.", '0.99'),
                     ('Paid $14.57 for groceries.', '14.57'),
                     ('Paid $14.57 for $5 worth of groceries. What a deal!', '14.57'),
                     ('Paid 45 bux for some turnips.', '45'),
                     )
        for message, expected in test_data:
            result = Message.get_money(message)
            print message,
            self.assertEqual(expected, result)
            print 'OK'


class TestTransaction(unittest.TestCase):
    def test___init__(self):
        # transaction = Transaction(amount, description, timestamp, category)
        self.skip("TODO: Not Implemented")

class TestPayCheck(unittest.TestCase):
    def test___init__(self):
        # pay_check = PayCheck(amount, description, timestamp, category, interval)
        self.skip("TODO: Not Implemented")

class TestBill(unittest.TestCase):
    def test___init__(self):
        # bill = Bill(amount, description, timestamp, category, interval)
        self.skip("TODO: Not Implemented")

class TestBudget(unittest.TestCase):
    def test___init__(self):
        # budget = Budget(name, interval, limit, description)
        self.skip("TODO: Not Implemented")

if __name__ == '__main__':
    unittest.main()
