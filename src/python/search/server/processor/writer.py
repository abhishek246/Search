'''
################################################################################
#   Writer                                                                     #
#   ======                                                                     #
#   Async Logging                                                              #
################################################################################
'''

import zmq

import logger
import utilities

from multiprocessing import Queue
from ConfigParser import ConfigParser

################################################################################
#   Global Variables                                                           #
################################################################################

conf = ConfigParser()
stage = ConfigParser()

################################################################################
#   Log Variables                                                              #
################################################################################

debug_q = Queue()
request_q = Queue()

log = logger.getLogger('Search-Writer')

debug_qhandler = logger.QueueHandler(debug_q)
request_qhandler = logger.QueueHandler(request_q)

debug = logger.WatchedFileHandler('/var/log/apps/search/debug.log')
request = logger.WatchedFileHandler('/var/log/apps/search/request.log')

pattern = '%(asctime)s : %(process)d : %(levelname)s : %(name)s : [%(lineno)d] %(message)s'

log.setLevel(10)
debug.setLevel(10)
request.setLevel(10)

request.setFormatter(logger.Formatter())
debug.setFormatter(logger.Formatter(pattern))

log.addHandler(debug_qhandler)

################################################################################
#   Thread Fucntions                                                           #
################################################################################

def e_thread():
    '''Main Event Loop'''

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
            if signal == 'shutdown_lv2':
                log.info('Shutdown Signal Received')
                main_running = 0
        except Exception, ex:
            log.exception(ex)

################################################################################
#   Utility Functions                                                          #
################################################################################

def load_config():
    '''Load App & Stage Config'''
    conf.read('/opt/localoye/search/search.conf')
    stage.read('/opt/localoye/search/stage.conf')

################################################################################
#   Logging Functions                                                          #
################################################################################

def start_logger():
    '''Start Queue Listeners'''
    global DEBUG_LOGGER, REQUEST_LOGGER

    DEBUG_LOGGER = logger.QueueListener(debug_q, debug)
    REQUEST_LOGGER = logger.QueueListener(request_q, request)

    utilities.set_threadname('L_THREAD')

    DEBUG_LOGGER.start()
    REQUEST_LOGGER.start()

def stop_logger():
    '''Stop Queue Listeners'''
    global DEBUG_LOGGER, REQUEST_LOGGER

    DEBUG_LOGGER.stop()
    REQUEST_LOGGER.stop()

################################################################################
#   Main Functions                                                             #
################################################################################

def f_process():
    '''Writer Main Function'''
    try:
        load_config()
        utilities.set_processname('Search Writer')

        log.info('Starting Up')
        start_logger()
        e_thread()

        log.info('Shutting Down')
        stop_logger()
    except Exception, ex:
        log.exception(ex)

    log.info('Shutdown Complete')
