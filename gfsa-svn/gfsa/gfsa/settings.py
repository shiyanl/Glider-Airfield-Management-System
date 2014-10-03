"""
Django settings for gfsa project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
#qUSE_TZ = True

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DIR = os.getcwd()
PAR_DIR = os.path.abspath('..')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n#-)6&k(6rv2es%0)gc*51o$6^2h5)vw_f3xz4ommt9n73$29@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '115.146.87.20']


# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gfsa',
    'flight',
    'tug',
    'glider',
    'xero',
    # 'south',
    'flarm',
    'clubs',
    # 'member'
    #'ajax_select',
)

AJAX_LOOKUP_CHANNELS = {
    #  simple: search Person.objects.filter(name__icontains=q)
    'person'  : {'model': 'xero.GFSAXeroContactPerson', 'search_field': 'first_name'},
    # define a custom lookup channel
    'song'   : ('example.lookups', 'SongLookup')
}
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    'django.contrib.messages.context_processors.messages',
    "django.core.context_processors.static",
)

ROOT_URLCONF = 'gfsa.urls'

WSGI_APPLICATION = 'gfsa.wsgi.application'
from django.contrib.messages import constants as messages
MESSAGE_TAGS= {messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'alert-danger danger'}

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'gfsa',  # Or path to database file if using sqlite3.
        'USER': 'root',  # Not used with sqlite3.
        'PASSWORD': 'gfsa_db_123',  # Not used with sqlite3.
        'HOST': '115.146.87.20',
        # '192.168.1.5',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',  #'3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'


TIME_ZONE = 'Australia/Melbourne'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Not used with sqlite3.

MEDIA_ROOT = DIR + '/gfsa/uploads'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/uploads/'



# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    PAR_DIR + '/static',

)

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    DIR + '/templates/',
)

NODE_NAME = 'YBSS'

SEAT_TYPE = (
    ('1', '1'),
    ('2', '2')
)

PAY_PERCENT = (
    ('0', '0'),
    ('50', '50'),
    ('100', '100')

)

STATUSES = (
    ('In Flight', 'In Flight'),
    ('Ready', 'Ready')

)
TEST_FLARM = True

