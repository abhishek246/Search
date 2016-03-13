'''
################################################################################
#   Utilities                                                                  #
#   =========                                                                  #
#   Search Utility Functions                                                   #
################################################################################
'''

import prctl
import ctypes

################################################################################
#   Utility Functions                                                          #
################################################################################

def set_processname(name):
    '''Set Process Name :: Linux'''
    prctl.set_name(name)
    prctl.set_proctitle(name)

def set_threadname(name):
    '''Set Thread Name :: Linux'''
    libc = ctypes.cdll.LoadLibrary('libc.so.6')
    libc.prctl(15, ctypes.c_char_p(name), 0, 0, 0)
