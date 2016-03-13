'''
################################################################################
#   Search Master                                                              #
#   =============                                                              #
#   Create and Destroy Stages                                                  #
################################################################################
'''

import zmq
import time
import signal

from multiprocessing import Process
from ConfigParser import ConfigParser

import sys
sys.path.append('../../../lib/python/')

from server.processor.writer import f_process as writer
from server.cognition import f_process as cognition

from django.core.management.base import BaseCommand, CommandError

import logger
import utilities

################################################################################ 
#   Global Variables                                                           #
################################################################################

conf = ConfigParser()
stage = ConfigParser()
process_master = {'cognition':cognition}

################################################################################
#   Log Variables                                                              #
################################################################################

log = logger.getLogger('Search')
monitor = logger.getLogger('Monitor')

form = logger.Formatter()
monitor_handler = logger.WatchedFileHandler('/var/log/apps/search/monitor.log')
monitor_handler.setLevel(10)
monitor_handler.setFormatter(form)
from server.processor.writer import debug_qhandler

log.setLevel(10)
monitor.setLevel(10)
log.addHandler(debug_qhandler)
monitor.addHandler(monitor_handler)

################################################################################
#   Signal Handlers                                                            #
################################################################################

def signal_handler(signum, stack):
    '''Signal Handler Method'''
    global MAIN_RUNNING, SOCKET
    if signum == signal.SIGTERM:
        try:
            MAIN_RUNNING = 0
        except Exception, ex:
            log.exception(ex)

signal.signal(signal.SIGTERM, signal_handler)

################################################################################
#   Thread Function                                                            #
################################################################################

def e_thread():
    '''Main Loop'''
    global MAIN_RUNNING, SOCKET

    utilities.set_threadname('Z_THREAD')

    context = zmq.Context()
    SOCKET = context.socket(zmq.PUB)
    SOCKET.bind('tcp://*:1234')

    utilities.set_threadname('E_THREAD')

    MAIN_RUNNING = 1
    while MAIN_RUNNING:
        try:
            time.sleep(0.99)
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
#   Main Functions                                                             #
################################################################################

def create_process():
    '''Fork Processes'''
    global WRITER, PROCESS_STAGE

    WRITER = Process(target=writer, args=())
    WRITER.start()

    PROCESS_STAGE = []
    for stage_name in stage.sections():
        process = Process(target=process_master.get(stage.get(stage_name,
                                                              'f_process')),
                          args=(stage_name,))
        PROCESS_STAGE.append(process)
        process.start()

def destroy_process():
    '''Join Processes'''
    global SOCKET, PROCESS_STAGE, WRITER

    # shutdown lv1
    #
    SOCKET.send('%s %s'%('signal', 'shutdown_lv1'))
    for process in PROCESS_STAGE:
        process.join()

    # shutdown lv2
    #
    SOCKET.send('%s %s'%('signal', 'shutdown_lv2'))
    WRITER.join()

################################################################################
#   Command Class                                                              #
################################################################################

class Command(BaseCommand):
    ''''''

    def handle(self, *args, **options):
        ''''''
        try:
            load_config()

            utilities.set_processname('Search Master')

            log.info('Starting Up')
            create_process()
            e_thread()

            log.info('Shutting Down')
            destroy_process()
        except Exception, ex:
            raise CommandError(ex)

        log.info('Shutdown Complete')
