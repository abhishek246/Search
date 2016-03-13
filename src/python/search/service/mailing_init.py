MAILING_CLIENT = None

def mailing_init(mail_client):
    global MAIL_CLIENT
    MAIL_CLIENT= mail_client

def get_mailclient():
    return MAIL_CLIENT
