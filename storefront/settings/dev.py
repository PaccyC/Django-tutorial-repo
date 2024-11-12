from .common import *


DEBUG = True


SECRET_KEY = 'django-insecure-)7x^6s2v3z^l+((=h!n-_pjb9-ai2&7ay8tf*y$bra227rr^bc'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront',
        'HOST': 'localhost',
        'USER': 'test',
        'PASSWORD': 'Paccy@123456789',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
