
import imaplib
import email

from settings import USE_IMAP, IMAP_SERVER, IMAP_PORT, IMAP_USE_SSL,\
                     ACCOUNT_NAME, PASSWORD, LABEL, EMAIL_ADDRESS

import pprint

def get_mail():
    if USE_IMAP:
        # Log in to the IMAP account.
        if IMAP_USE_SSL:
            mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        else:
            mail = imaplib.IMAP4(IMAP_SERVER, IMAP_PORT)

        mail.login(ACCOUNT_NAME, PASSWORD)

        mail.select(LABEL or "inbox")

        # Get all mail from the user
        result, data = mail.uid('search', None, '(FROM "%s")' % EMAIL_ADDRESS)
        data = data[0].split()
        if result == "OK":
            for uid in data:
                result, data = mail.uid('fetch', uid, '(RFC822)')
                if result == "OK":
                    raw_email = data[0][1]
                    email_message = email.message_from_string(raw_email)
                    yield email_message['Subject']

if __name__ == "__main__":
    for message in get_mail():
        print message
