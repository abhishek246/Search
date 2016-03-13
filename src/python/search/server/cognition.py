'''
################################################################################
#   Cognition                                                                  #
#   =========                                                                  #
#   Cognitive Server for Search                                                #
################################################################################
'''

import gevent
import zerorpc
import zmq.green as zmq

import logger
import utilities
from ConfigParser import ConfigParser
from service import SearchRPC
from service import mobilepush_init, mailing_init, batwaa_init

################################################################################
#   Global Variables                                                           #
################################################################################

conf = ConfigParser()
stage = ConfigParser()

################################################################################
#   Log Variables                                                              #
################################################################################

log = logger.getLogger('Search-Cognition')
search = logger.getLogger('Cognition')

from server.processor.writer import debug_qhandler, request_qhandler

log.setLevel(10)
search.setLevel(10)
log.addHandler(debug_qhandler)
search.addHandler(request_qhandler)

################################################################################
#   Thread Function                                                            #
################################################################################

def e_thread():
    '''ZeroMQ Event Listner'''
    global SERVER

    utilities.set_threadname('Z_THREAD')

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect('tcp://localhost:1234')
    socket.setsockopt(zmq.SUBSCRIBE, 'signal')

    utilities.set_threadname('E_THREAD')

    main_running = 1
    while main_running:
        try:
            data = socket.recv()
            signal_type, signal = data.split()
            if signal == 'shutdown_lv1':
                log.info('Shutdown Signal Received')
                SERVER.stop()
                main_running = 0
        except Exception, ex:
            log.exception(ex)

def f_thread(stage_name):
    '''ZeroRPC Search Service'''
    global SERVER
    utilities.set_threadname('G_THREAD')
    port = stage.get(stage_name, 'port')
    endpoint = ':'.join(('tcp', '//127.0.0.1', port))
    log.info('Port: ' + str(port))
    SERVER = zerorpc.Server(SearchRPC(mobilepush_client, mailing_client, batwaa_client))
    mobilepush_init.mobilepush_init(mobilepush_client)
    mailing_init.mailing_init(mailing_client)
    batwaa_init.batwaa_init(batwaa_client)
    SERVER.bind(endpoint)
    SERVER.run()

################################################################################
#   Utility Functions                                                          #
################################################################################

def load_config():
    '''Load App & Stage Config'''
    global mobilepush_client, mailing_client, batwaa_client
    from django.conf import settings
    mobilepush_client = zerorpc.Client()
    mobilepush_client.connect(settings.MOBILEPUSH_URL)
    mailing_client = zerorpc.Client()
    mailing_client.connect(settings.MAIL_URL)
    batwaa_client = zerorpc.Client()
    batwaa_client.connect(settings.BATWAA_URL)
    conf.read('/opt/localoye/search/search.conf')
    stage.read('/opt/localoye/search/stage.conf')

################################################################################
#   Main Functions                                                             #
################################################################################

def f_process(stage_name):
    '''Cognition Search Main Function'''
    try:
        load_config()
        utilities.set_processname('Search Cognition')

        log.info('Starting Up')
        gevent.spawn(e_thread)
        f_thread(stage_name)

        log.info('Shutting Down')
    except Exception, ex:
        log.exception(ex)

    log.info('Shutdown Complete')
