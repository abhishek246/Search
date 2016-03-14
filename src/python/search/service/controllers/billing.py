'''
#######################################################
#
#######################################################
'''

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
################################################################################
#
################################################################################

import logger

log = logger.getLogger('Search-Cognition')

################################################################################
#
################################################################################


def handle_db_exceptions(query_func):
    '''Decorator for Handling Exception in Query Functions.'''
    def inner(*args, **kwargs):
        try:
            return query_func(*args, **kwargs)
        except ObjectDoesNotExist, ex:
            log.info('ObjectDoesNotExist Exception occured in %s.' % query_func.__name__)
            log.exception(ex)
        except InterfaceError, ex:
            log.info('InterfaceError Exception occured in %s.' % query_func.__name__)
            log.exception(ex)
            close_connection()
            return query_func(*args, **kwargs)
        except OperationalError, ex:
            log.info('OperationalError Exception occured in %s.' % query_func.__name__)
            log.exception(ex)
            close_connection()
            return query_func(*args, **kwargs)
    return inner


@handle_db_exceptions
def _city_center():
    try:
        return 'Center'
    except Exception, ex:
        log.exception(ex)
