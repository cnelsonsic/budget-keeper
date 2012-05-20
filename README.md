budget-keeper
=============

[![Build Status](https://secure.travis-ci.org/cnelsonsic/budget-keeper.png?branch=master)](http://travis-ci.org/cnelsonsic/budget-keeper)

A tiny webapp for keeping a budget.

budget-keeper tracks your expenditures via simple email messages.

At its core, it's just a fancy email client that looks for messages
you send to it that look like notes for your purchases and expenses.


Usage
-----

Send yourself an email with a subject like "Paid $14.57 for Groceries."
budget-keeper will then add a $14.57 entry to the budget category "Groceries".
Sticking to a well-formed format will ensure the best recognition of your data.
You can get pretty free-form with your formatting, but if you enter something
without an obvious category, it will just be entered in as a general expense.

As far as formatting money goes, it can pick up pretty much anything you throw at it, as long as it's a number.
The following are some known working examples:
'$4.12', '$4', '.12', '100'

The following format will enter expenditures into budget categories (presuming the category exists):
'Paid $14.57 for groceries.'

If you're feeling particularly terse:
'$100 groceries'

Multiple purchases are also supported. But keep in mind the parser is pretty fragile, so try not to deviate from the examples much:
'Paid $14.57 for groceries and paid $61.00 for shoes.'

These formats will not match budget categories, but will enter expenditures into your account:
'Paid $14.57 for a book from the used bookstore.'
"Bought a new pair of pants for $5. Quite a steal."
"[18:34] <joe> I bought a new widget today, was only $0.99"

