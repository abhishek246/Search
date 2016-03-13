from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'NAME': 'billing',
        'USER': 'root',
        'PASSWORD': 'local',
        'HOST': 'localhost',
        'PORT': '3306',
        'CONN_MAX_AGE': 86400,

    }
}

MOBILEPUSH_URL = 'tcp://127.0.0.1:8020'
MAIL_URL = 'tcp://127.0.0.1:8000'
BATWAA_URL = 'tcp://127.0.0.1:6900'
COMMUNICATION_URL = 'tcp://127.0.0.1:7200'
ALARM_SERVICE_URL = 'tcp://127.0.0.1:5001'
PAYMENT_URL = 'tcp://127.0.0.1:6800'
SEARCH_IP = '127.0.0.1'
