
import imaplib
import email

import settings

def get_mail():
    if settings.IMAP_ENABLED:
        # Log in to the IMAP account.
        if settings.IMAP_USE_SSL:
            mail = imaplib.IMAP4_SSL(settings.IMAP_SERVER, settings.IMAP_PORT)
        else:
            mail = imaplib.IMAP4(settings.IMAP_SERVER, settings.IMAP_PORT)

        mail.login(settings.AUTHENTICATION_EMAIL, settings.AUTHENTICATION_PASSWORD)

        mail.select(settings.IMAP_LABEL or "inbox")

        # Get all mail from the user
        result, data = mail.uid('search', None, '(FROM "%s")' % settings.AUTHENTICATION_EMAIL)
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
