from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'NAME': 'localoye',
        'USER': 'localoye',
        'PASSWORD': 'localoye',
        'HOST': 'localhost',
        'PORT': '3306',
        'CONN_MAX_AGE': 86400,

    },
    'payment': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'NAME': 'localoye_payment',
        'USER': 'localoye',
        'PASSWORD': 'localoye',
        'HOST': 'localhost',
        'PORT': '3306',
        'CONN_MAX_AGE': 86400,

    },
    'ops': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'NAME': 'localoye_ops',
        'USER': 'localoye',
        'PASSWORD': 'localoye',
        'HOST': 'localhost',
        'PORT': '3306',
        'CONN_MAX_AGE': 86400,
    }
}

MOBILEPUSH_URL = 'tcp://127.0.0.1:8020'
MAIL_URL = 'tcp://127.0.0.1:8000'
BATWAA_URL = 'tcp://127.0.0.1:6900'
