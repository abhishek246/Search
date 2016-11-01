'''
#######################################################
#
#######################################################
'''

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from service.models import City, DropPoint, Agent
from service.models import City, DropPoint
from django.db import InterfaceError, OperationalError, close_connection

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
            log.info('ObjectDoesNotExist Exception occured in %s.'
                % query_func.__name__)
            log.exception(ex)
        except InterfaceError, ex:
            log.info('InterfaceError Exception occured in %s.'
                % query_func.__name__)
            log.exception(ex)
            close_connection()
            return query_func(*args, **kwargs)
        except OperationalError, ex:
            log.info('OperationalError Exception occured in %s.'
                % query_func.__name__)
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

        try:
            cities = City.objects.filter(is_active=True)
        except Exception, ex:
            log.exception(ex)

        city_list = []
        for city in cities:
            centers = DropPoint.objects.filter()
            center_list = []
            for center in centers:
                center_list.append({
                    'center_name': center.name,
                    'center_slug': center.slug_name
                })
            city_list.append({
                'city_name': city.name,
                'city_slug': city.slug_name,
                'center_list': center_list
            })

        if len(city_list) > 0:
            return city_list

        return {'message': 'Revlavent City data does not exists',
                'error': 'Data Error'
            }
    except Exception, ex:
        log.exception(ex)

@handle_db_exceptions
def _agent_details():
    '''get all agent details'''
    try:
        return 'this is agent details abc'
    except Exception, ex:
        log.exception(ex)

@handle_db_exceptions
def _add_agent(kwargs):
    _query = {
        'name': kwargs.get('name'),
        'area': kwargs.get('area')
    }
    agent = {'status':'Successfully Created'}
    try:
        _agent = Agent.objects.get(**_query)
        agent = {'status':'User Already exists'}
    except Agent.DoesNotExist as ex:
        _agent = Agent.objects.create(**query)
    return agent

@handle_db_exceptions
def _add_indent(kwargs):
    _agent_query = {
        'agent': kwargs.get('agent'),
        'is_active': True
    }
    _paper_query = {
        'name_slug': kwargs.get('paper'),
        'is_active': True
    }
    try:
        _agent = Agent.objects.get(**_agent_query)
        _paper = NewsPaper.objects.get(**_paper_query)
    except (Agent.DoesNotExist, NewsPaper.DoesNotExist) as ex:
        log.exception('--> %s agent or newpaper does not exists', __name__)

    #with transaction.atmoic():
    _indent = kwargs('indent')
    for data in _indent:
        try:
            _query = {
                'agent': _agent,
                'newspaper': _paper,
                'date': data.get('date')
            }
            indent = Indent.objects.get(**_query)
        except Indent.DoesNotExist as ex:
            indent = Indent(agent=_agent, newspaper=_paper, date=data.get('date'), indent=int(data.get('quantity')))
        else:
            setattr(indent, 'indent', int(data.get('quantity')))
            indent.save()
    return {'status': 'Successfully Updated Indent'}
