import os
from .settings import BASE_DIR

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'plutus',
#        'USER': 'webusr',
#        'PASSWORD': '&./Z%z$zUpdt$3~6',
#        'HOST': '127.0.0.1',
#   }
#}

# Live Settings
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'provisn',
#        'USER': 'webusr',
#        'PASSWORD': 'q7WB/WeYY+RSWyHP',
#        'HOST': '127.0.0.1',
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}