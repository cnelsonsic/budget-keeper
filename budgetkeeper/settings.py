
# Shared settings:
ACCOUNT_NAME = "example@gmail.com"
EMAIL_ADDRESS = ACCOUNT_NAME
PASSWORD = "testpassword"

# These two options are mutually exclusive.
# IMAP is preferred, but your email server may
# not support it.
USE_IMAP = True
USE_POP = False

# SMTP Settings:
SMTP_SERVER = 'smtp.gmail.com'
SMTP_USE_AUTHENTICATION = True
USE_STARTTLS = True # Or SSL
TLS_PORT = 587
SSL_PORT = 465

# IMAP Settings:
IMAP_SERVER = 'imap.gmail.com'
IMAP_USE_SSL = True
IMAP_PORT = 993

# POP Settings:
POP_SERVER = 'pop.gmail.com'
POP_USE_SSL = True
POP_PORT = 995

# Budget-keeper folder/label
# Set this on your incoming mail with a filter or somesuch
# And budget-keeper will only look at those mails.
# By default, it just looks at your inbox (archived mail should be ignored)
# LABEL = 'budget-keeper'
LABEL = False
