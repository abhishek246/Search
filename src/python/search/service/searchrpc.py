'''
################################################################################
#   SearchRPC                                                                  #
#   =========                                                                  #
#                                                                              #
################################################################################
'''

import time
from controllers import *

################################################################################
#   Log Variables                                                              #
################################################################################

import logger

log = logger.getLogger('Search-Cognition')

################################################################################
#   Global Functions                                                           #
################################################################################

def log_service(func):
    def inner(*args, **kwargs):
        log.info('%s Started.' % func.__name__)
        start_time = time.time()
        result = func(*args, **kwargs)
        log.info('%s Ended. Time Taken: %s' % (func.__name__, int(round(time.time()*1000)) - int(round(start_time*1000))))
        return result
    return inner

################################################################################
#   Search Service Class                                                       #
################################################################################

class SearchRPC(object):
    ''''''
    @log_service
    def __init__(self, mobilepush_client, mailing_client, batwaa_client):
        self.mobilepush_client = mobilepush_client
        self.mailing_client = mailing_client
        self.batwaa_client = batwaa_client

    @log_service
    def run_check(self):
        try:
            return 'Search Running @ port 9000'
        except Exception, ex:
            log.exception(ex)

    @log_service
    def city_center(self):
        try:
            return _city_center()
        except Exception,ex:
            log.exception(ex)

    @log_service
    def agent_details(self):
        ''' Public Function  '''
        try:
            return _agent_details()
        except Exception,ex:
            log.exception(ex)

    @log_service
    def add_agent(self):
        return _add_agent()
