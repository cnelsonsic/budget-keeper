
import re
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
    Income(amount=Decimal('100'), category=None, description='Gift from Grandma', timestamp=datetime.datetime(2012, 1, 1, 0, 0))

    And check your current balance.
    >>> account.balance
    Decimal('100.00')

    It also keeps track of daily expenses:
    >>> account.add_purchase(4.12, description="Morning Coffee", timestamp=datetime.datetime(2012, 1, 1))
    Purchase(amount=Decimal('4.12'), category=None, description='Morning Coffee', timestamp=datetime.datetime(2012, 1, 1, 0, 0))

    As well as bills recurring on an interval:
    >>> account.add_bill(100.00, description="Internet", interval=MONTHLY, timestamp=datetime.datetime(2012, 1, 1))
    Bill(amount=Decimal('100'), category=None, description='Internet', interval=relativedelta(months=+1), timestamp=datetime.datetime(2012, 1, 1, 0, 0))

    And also paychecks (income on an interval):
    >>> account.add_paycheck(1000.00, description="Paycheck from WebApps Inc.", interval=BIMONTHLY, timestamp=datetime.datetime(2012, 1, 1))
    PayCheck(amount=Decimal('1000'), category=None, description='Paycheck from WebApps Inc.', interval=relativedelta(days=+14), timestamp=datetime.datetime(2012, 1, 1, 0, 0))

    Adding a budget for something is easy enough:
    >>> account.add_budget('Groceries', interval=MONTHLY, limit=100, description="Monthly grocery allowance.")
    Budget(description='Monthly grocery allowance.', interval=relativedelta(months=+1), limit=Decimal('100'), name='Groceries')

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
        purchase = Purchase(amount=Decimal(amount).quantize(Decimal('0.01')),
                            description=description,
                            timestamp=timestamp,
                            category=category)
        self.transactions.append(purchase)
        return purchase

    def add_bill(self, amount, description="", timestamp=None, category=None, interval=None):
        bill = Bill(amount=Decimal(amount), description=description, timestamp=timestamp, category=category, interval=interval)
        self.transactions.append(bill)
        return bill

    def add_paycheck(self, amount, description="", timestamp=None, category=None, interval=None):
        paycheck = PayCheck(amount=Decimal(amount), description=description, timestamp=timestamp, category=category, interval=interval)
        self.transactions.append(paycheck)
        return paycheck

    def parse_message(self, message, timestamp=None):
        '''
        >>> account = Account()

        It will also parse emails and other messages like so:
        The ideal format is "Paid ${money} for ${description}"
        >>> account.parse_message('Paid $14.57 for a book from the used bookstore.') # doctest: +ELLIPSIS
        Purchase(amount=Decimal('14.57'), category=None, description='A book from the used bookstore.', ...)

        Another format is like "Bought ${description} for ${money} ${more_description}"
        >>> account.parse_message("Bought a new pair of pants for $5. Quite a steal.") # doctest: +ELLIPSIS
        Purchase(amount=Decimal('5.00'), category=None, description='A new pair of pants. Quite a steal.', ...)

        Sometimes it's not smart enough to parse out a meaningful description,
        so it just uses the whole thing.
        >>> account.parse_message("[18:34] <joe> I bought a new widget today, was only $0.99") # doctest: +ELLIPSIS
        Purchase(amount=Decimal('0.99'), category=None, description='[18:34] <joe> I bought a new widget today, was only $0.99', ...)

        Adding budget categories is easy too, as long as it matches a budget category:
        The ideal format is "Paid ${money} for ${budget_category}"
        >>> _ = account.add_budget('Groceries', interval=MONTHLY, limit=100, description="Monthly grocery allowance.")
        >>> account.parse_message('Paid $14.57 for groceries.') # doctest: +ELLIPSIS
        Purchase(amount=Decimal('14.57'), category='Groceries', ...)

        Not enough time to type out a windy description? Works fine too:
        >>> account.parse_message('100 groceries') # doctest: +ELLIPSIS
        Purchase(amount=Decimal('100.00'), category='Groceries', ...)

        You can also embed the category in a windy description.
        >>> account.parse_message('Paid $100 for some groceries because I hunger.') # doctest: +ELLIPSIS
        Purchase(amount=Decimal('100.00'), category='Groceries', description='Some groceries because i hunger.', ...)

        You can also add multiple expenditures to multiple categories:
        >>> _ = account.add_budget('Groceries', interval=MONTHLY, limit=100, description="Monthly grocery allowance.")
        >>> _ = account.add_budget('Booze', interval=MONTHLY, limit=100, description="Monthly booze allowance.")
        >>> account.parse_message('Paid $14.57 for groceries and paid $50 for booze.') # doctest: +ELLIPSIS
        [Purchase(amount=Decimal('14.57'), category='Groceries', ...), Purchase(amount=Decimal('50.00'), category='Booze', ...)]
        '''
        parts = message.split('and')
        purchases = []
        for message in parts:
            amount = Message.get_money(message)
            if not amount:
                return

            description = Message.get_description(message)

            purchase = None

            # Is any of our budget names in the description?
            for budget in self.budgets:
                # if description (minus nonletter characters) in categories:
                category = re.sub(r'[^\w]*', '', description).lower()
                if budget.name.lower() in category.lower():
                    # Set the category instead of the description
                    description = '' if budget.name.lower() == category.lower() else description
                    purchase = self.add_purchase(amount, category=budget.name, timestamp=timestamp, description=description)
                    break

            purchases.append(purchase or self.add_purchase(amount, description, timestamp))
        return purchases[0] if len(purchases) == 1 else purchases

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
        >>> account.add_purchase(100, description='Morning Coffee', category='Thing', timestamp=datetime.datetime(2012, 1, 1))
        Purchase(amount=Decimal('100.00'), category='Thing', description='Morning Coffee', timestamp=datetime.datetime(2012, 1, 1, 0, 0))
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

class Message(object):
    money = r'\$?(\d*(\.\d\d?)?|\d+)'
    only_money = re.compile(r'^%s.*$' % money)

    @staticmethod
    def get_money(message):
        '''Gets the first thing that looks like money from a message.
        >>> Message.get_money('$4.12')
        '4.12'
        >>> Message.get_money('4.12')
        '4.12'
        >>> Message.get_money("[18:34] <joe> I bought a new widget today, was only $0.99.")
        '0.99'
        '''
        for word in message.split(' '):
            result = Message.only_money.findall(word)[0][0]
            if result:
                return result

    @staticmethod
    def get_description(message):
        '''
        It will also parse emails and other messages like so:
        The ideal format is "Paid ${money} for ${description}"
        >>> Message.get_description('Paid $14.57 for a book from the used bookstore.')
        'A book from the used bookstore.'

        Adding budget categories is easy too, as long as it matches a budget category:
        The ideal format is "Paid ${money} for ${budget_category}"
        >>> Message.get_description('Paid $14.57 for groceries.')
        'Groceries.'

        Another format is like "Bought ${description} for ${money} ${more_description}"
        >>> Message.get_description("Bought a new pair of pants for $5. Quite a steal.")
        'A new pair of pants. Quite a steal.'

        Sometimes it's not smart enough to parse out a meaningful description,
        so it just uses the whole thing.
        >>> Message.get_description("[18:34] <joe> I bought a new widget today, was only $0.99")
        '[18:34] <joe> I bought a new widget today, was only $0.99'
        '''
        # TODO: pyparsing may be the way to go here.

        # Try to match the well behaved version first:
        description = re.match(r'(?:paid )?(?:bought )?(?P<first_desc>.*) for (?P<description>.*)', message.lower(), flags=re.IGNORECASE)
        if description:
            # If the first part of the description is actually money,
            # Then use this well behaved version, if it's actually more
            # description, move on to the extended description version.
            first_desc_is_money = Message.get_money(description.group('first_desc'))
            if description.group('description') and first_desc_is_money:
                return description.group('description').capitalize()

        # Try getting the extended description version:
        # Remove the money from the message.
        money = Message.get_money(message)
        if not money:
            # Couldn't get a money from the message
            return

        regex = r"( ?\$?(%s)[ ]?)" % re.escape(money)
        msg = re.sub(regex, '', message, count=1)

        # Now grab all the parts of our description.
        ext_desc = r'bought (?P<description>.*) for[ ]?(?P<more_description>.*)'
        extended_desc = re.match(ext_desc, msg, flags=re.IGNORECASE)
        if extended_desc:
            if extended_desc.group('description') or extended_desc.group('more_description'):
                return (extended_desc.group('description').capitalize() + extended_desc.group('more_description'))

        # Nothing matched, just return the whole thing.
        return message


class ReprableClass(object):
    def __repr__(self):
        kwargs = ', '.join(['%s=%r' % (attrib, getattr(self, attrib)) for attrib in sorted(vars(self).keys())])
        return "%s(%s)" % (self.__class__.__name__, kwargs)

class Budget(ReprableClass):
    '''Budgets are categories that purchases fall under.
    '''
    def __init__(self, name, interval=None, limit=100, description=""):
        self.name = name
        self.interval = interval
        self.limit = limit
        self.description = description

class Transaction(ReprableClass):
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

def main():
    '''Checks a mail account for new messages since the last time it checked,
    and parse them for the account information.
    Should be called on a cron.'''
    from get_mail import get_mail
    account = Account()
    for message in get_mail():
        print message
        account.parse_message(message)

    print account.balance

if __name__ == "__main__":
    main()
