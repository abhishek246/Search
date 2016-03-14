'''
#######################################################
#
#######################################################
'''

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from service.models import City, DropPoint

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

######################################################
#
#######################################################

@handle_db_exceptions
def _city_center():
    ''' All city and center related to that city'''
    try:
        cities = City.objects.all()
        city_list = []
        for city in cities:
            city_list.append({
                'city_name': city.name,
                'city_slug': city.slug_name
            })
        return city_list
    except Exception, ex:
        log.exception(ex)

@handle_db_exceptions
def _agent_details():
    '''get all agent details'''
    try:
        return 'agent details'
    except Exception, ex:
        log.exception(ex)
