
import datetime
from dateutil.relativedelta import relativedelta

MONTHLY = relativedelta(months=1)
BIWEEKLY = relativedelta(weeks=2)
BIMONTHLY = BIWEEKLY # I never really did understand this, but whatever.
DAILY = relativedelta(days=1)
ANNUALLY = relativedelta(years=1)

try:
    from cDecimal import Decimal
except ImportError:
    from decimal import Decimal

class Account(object):
    '''Account contains transactions, which keep track of income and expenses.

    >>> account = Account()

    You can add a one-time income to your account like so:
    >>> account.add_income(100.00, description="Gift from Grandma", timestamp=datetime.datetime(2012, 1, 1))
    Income(amount=Decimal('100'), description='Gift from Grandma', timestamp=datetime.datetime(2012, 1, 1, 0, 0), category=None)

    And check your current balance.
    >>> account.balance
    Decimal('100.00')

    It also keeps track of daily expenses:
    >>> account.add_purchase(4.12, description="Morning Coffee")

    As well as bills recurring on an interval:
    >>> account.add_bill(100.00, description="Internet", interval=MONTHLY, timestamp=datetime.datetime(2012, 1, 1))
    Bill(amount=Decimal('100'), description='Internet', timestamp=datetime.datetime(2012, 1, 1, 0, 0), category=None, interval=relativedelta(months=+1))

    And also paychecks (income on an interval):
    >>> account.add_paycheck(1000.00, description="Paycheck from WebApps Inc.", interval=BIMONTHLY)

    Adding a budget for something is easy enough:
    >>> account.add_budget('Groceries', interval=MONTHLY, limit=100, description="Monthly grocery allowance.")
    Budget(name='Groceries', interval=relativedelta(months=+1), limit=Decimal('100'), description='Monthly grocery allowance.')

    Note that adding a recurring debit or credit will add it to your account balance immediately.
    It WILL NOT wait for the next recurrance.

    Getting the balance is just this easy:
    >>> account.balance
    Decimal('995.88')

    '''
    def __init__(self):
        self.transactions = []
        self.budgets = []

        # TODO: Load everything from disk

    @property
    def balance(self):
        total = sum([trans.amount*trans.direction for trans in self.transactions])
        return Decimal(total).quantize(Decimal('0.01'))

    def add_income(self, amount, description="", timestamp=None, category=None):
        income = Income(amount=Decimal(amount), description=description, timestamp=timestamp, category=category)
        self.transactions.append(income)
        return income

    def add_purchase(self, amount, description="", timestamp=None, category=None):
        purchase = Purchase(amount=Decimal(amount), description=description, timestamp=timestamp, category=category)
        self.transactions.append(purchase)

    def add_bill(self, amount, description="", timestamp=None, category=None, interval=None):
        bill = Bill(amount=Decimal(amount), description=description, timestamp=timestamp, category=category, interval=interval)
        self.transactions.append(bill)
        return bill

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

        Adding budget categories is easy too, as long as it matches a budget category:
        The ideal format is "Paid ${money} for ${budget_category}"
        >>> account.parse_message('Paid $14.57 for groceries.')
        Purchase(amount=14.57, category='groceries')
        '''
        pass

    def trigger_recurring(self, timestamp=None):
        '''Trigger all recurring transactions.'''
        pass

    def add_budget(self, name, interval=None, limit=100, description=""):
        budget = Budget(name=name, interval=interval, limit=Decimal(limit), description=description)
        self.budgets.append(budget)
        return budget

    def get_budget_totals(self):
        '''Get a dict of totals for all budgets.
        >>> account = Account()
        >>> budget = account.add_budget('Thing')
        >>> account.add_purchase(100, description='Morning Coffee', category='Thing')
        >>> account.get_budget_totals()
        {'Thing': Decimal('100.00')}
        '''
        totals = {}
        for budget in self.budgets:
            totals[budget.name] = 0
            for purchase in self.transactions:
                if purchase.direction < 0: # If its direction says its a debit
                    if purchase.category == budget.name:
                        totals[budget.name] += purchase.amount
            totals[budget.name] = totals[budget.name].quantize(Decimal('0.01'))
        return totals


class Budget(object):
    '''Budgets are categories that purchases fall under.
    '''
    def __init__(self, name, interval=None, limit=100, description=""):
        self.name = name
        self.interval = interval
        self.limit = limit
        self.description = description

    def __repr__(self):
        return 'Budget(name=%(name)r, interval=%(interval)r, limit=%(limit)r, description=%(description)r)' % self.__dict__

class Transaction(object):
    '''Transactions are any money going in or out of an Account.'''
    direction = 0
    def __init__(self, amount=0, description="", timestamp=None, category=None):
        if not timestamp:
            timestamp = datetime.datetime.now()
        self.timestamp = timestamp
        self.amount = amount
        self.description = description
        self.category = category

class Income(Transaction):
    '''Income is money going into the account.'''
    direction = +1

    def __repr__(self):
        return "Income(amount=%(amount)r, description=%(description)r, timestamp=%(timestamp)r, category=%(category)r)" % self.__dict__

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

    def __repr__(self):
        return 'Bill(amount=%(amount)r, description=%(description)r, timestamp=%(timestamp)r, category=%(category)r, interval=%(interval)r)' % self.__dict__

