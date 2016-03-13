MOBILEPUSH_CLIENT = None

def mobilepush_init(mobilepush_client):
    global MOBILEPUSH_CLIENT
    MOBILEPUSH_CLIENT = mobilepush_client

def get_mobilepush():
    return MOBILEPUSH_CLIENT
