
import datetime
from dateutil.relativedelta import relativedelta

try:
    from cDecimal import Decimal
except ImportError:
    from decimal import Decimal

class Account(object):
    '''Account contains transactions, which keep track of income and expenses.

    >>> account = Account()

    You can add a one-time income to your account like so:
    >>> account.add_income(100.00, description="Gift from Grandma")

    And check your current balance.
    >>> account.balance
    Decimal('100.00')

    It also keeps track of daily expenses:
    >>> account.add_purchase(4.12, description="Morning Coffee")

    As well as bills recurring on an interval:
    >>> monthly = relativedelta(months=1)
    >>> account.add_bill(100.00, description="Internet", interval=monthly)

    And also paychecks (income on an interval):
    >>> bimonthly = relativedelta(weeks=2)
    >>> account.add_paycheck(1000.00, description="Paycheck from WebApps Inc.", interval=bimonthly)

    Note that adding a recurring debit or credit will add it to your account balance immediately.
    It WILL NOT wait for the next recurrance.

    >>> account.balance
    Decimal('995.88')

    '''
    def __init__(self):
        self.transactions = []

        # TODO: Load everything from disk

    @property
    def balance(self):
        total = sum([trans.amount*trans.direction for trans in self.transactions])
        return Decimal(total).quantize(Decimal('0.01'))

    def add_income(self, amount, description="", timestamp=None, category=None):
        income = Income(amount=Decimal(amount), description=description, timestamp=timestamp, category=category)
        self.transactions.append(income)

    def add_purchase(self, amount, description="", timestamp=None, category=None):
        purchase = Purchase(amount=Decimal(amount), description=description, timestamp=timestamp, category=category)
        self.transactions.append(purchase)

    def add_bill(self, amount, description="", timestamp=None, category=None, interval=None):
        bill = Bill(amount=Decimal(amount), description=description, timestamp=timestamp, category=category, interval=interval)
        self.transactions.append(bill)

    def add_paycheck(self, amount, description="", timestamp=None, category=None, interval=None):
        paycheck = PayCheck(amount=Decimal(amount), description=description, timestamp=timestamp, category=category, interval=interval)
        self.transactions.append(paycheck)

    def parse_message(self, message):
        '''
        >>> account = Account()

        It will also parse emails and other messages like so:
        The ideal format is "Paid ${money} for ${description}"
        >>> account.parse_message('Paid $14.57 for a book from the used bookstore.')
        Purchase(amount=14.57, description="A book from the used bookstore.')

        Another format is like "Bought ${description} for ${money} ${more_description}"
        >>> account.parse_message("Bought a new pair of pants for $5. Quite a steal.")
        Purchase(amount=5, description="A new pair of pants. Quite a steal.")

        Sometimes it's not smart enough to parse out a meaningful description,
        so it just uses the whole thing.
        >>> account.parse_message("[18:34] <joe> I bought a new widget today, was only $0.99")
        Purchase(amount=0.99, description="I bought a new widget today, was only $0.99")
        '''
        pass

    def trigger_recurring(self, timestamp=None):
        '''Trigger all recurring transactions.'''
        pass


class Transaction(object):
    '''Transactions are any money going in or out of an Account.'''
    direction = 0
    def __init__(self, amount=0, description="", timestamp=None, category=None):
        if not timestamp:
            timestamp = datetime.datetime.now()
        self.amount = amount
        self.description = description
        self.category = category

class Income(Transaction):
    '''Income is money going into the account.'''
    direction = +1

class Purchase(Transaction):
    '''An Expense is money going out of the account.'''
    direction = -1

class PayCheck(Income):
    '''A Paycheck is income that is deposited on a recurring basis.'''
    def __init__(self, amount, description="", timestamp=None, category=None, interval=None):
        super(PayCheck, self).__init__(amount=amount, description=description,
                                       timestamp=timestamp, category=category)
        self.interval = interval

class Bill(Purchase):
    '''A Bill is a purchase that is made on a recurring basis.'''
    def __init__(self, amount, description="", timestamp=None, category=None, interval=None):
        super(Bill, self).__init__(amount=amount, description=description,
                                   timestamp=timestamp, category=category)
        self.interval = interval

