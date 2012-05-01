#!/bin/env python
'''This script runs a web process to interact with your Account.'''

from budgetkeeper import Account

import tornado.ioloop
import tornado.web

class AccountHandler(tornado.web.RequestHandler):
    def get(self):
        account = Account()
        # TODO: Render the template with this account object.

class BalanceView(tornado.web.RequestHandler):
    def get(self):
        self.write(Account().balance)

application = tornado.web.Application([
    (r"/", AccountHandler),
    (r"/balance", BalanceView),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
