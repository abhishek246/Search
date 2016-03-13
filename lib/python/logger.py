'''
################################################################################
#   Logger                                                                     #
#   ======                                                                     #
#   Search Logging Utility Functions                                           #
################################################################################
'''

import logging

from logging import handlers
from logutils import queue

################################################################################
#   Global Variables                                                           #
################################################################################

log_level = [logging.NOTSET,
             logging.DEBUG,
             logging.INFO,
             logging.WARNING,
             logging.ERROR,
             logging.CRITICAL]

################################################################################
#   Logging Functions                                                          #
################################################################################

def getLogger(name):
    '''Return a logger instance'''
    return logging.getLogger(name)

def Formatter(fmt='%(asctime)s : %(message)s', datefmt='%Y-%m-%d %H:%M:%S'):
    '''Return a Formatter instance'''
    return logging.Formatter(fmt, datefmt)

def NullHandler():
    '''Return a NullHandlerinstance'''
    return logging.NullHandler()

def WatchedFileHandler(filename):
    '''Return a WatchedFileHandler instance'''
    return handlers.WatchedFileHandler(filename)

def QueueHandler(mqueue):
    '''Return a QueueHandler instance'''
    return queue.QueueHandler(mqueue)

def QueueListener(mqueue, handler):
    '''Return a QueueListener instance'''
    return queue.QueueListener(mqueue, handler)
