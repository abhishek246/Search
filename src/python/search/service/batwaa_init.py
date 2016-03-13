BATWAA_CLIENT = None

def batwaa_init(batwaa_client):
    global BATWAA_CLIENT
    BATWAA_CLIENT= batwaa_client

def get_batwaa_client():
    return BATWAA_CLIENT
