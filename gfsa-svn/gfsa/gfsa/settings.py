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

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'gfsatrail.cloudapp.net']


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
    'flarm',
    'clubs',
    'ajax_select',
    'django_crontab',
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
        'PASSWORD': 'gfsa123456',  # Not used with sqlite3.
        'HOST': '',
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
#Flarm configure
FLARM_DOMAIN = "www.flarmradar.ch"
FLARM_NODE_NAME = 'YBSS'
#
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
TEST_FLARM = False

# Settings for automation, you can replace the frequency with below ones.
# Just remember that any changes on crontab, you must run the command 
# "python manage.py crontab remove" first and then "python manage.py crontab add" 
PER_HOUR = '* */1 * * *'
PER_MINUTE = '*/1 * * * *'
PER_DAY = '* * */1 * *'
FIX_TIME = '* 17 * * *' # 17:00 everyday

XERO_FREQ_UPDATE_CONTACTS = FIX_TIME
XERO_FREQ_UPDATE_ITEMCODES = FIX_TIME
XERO_FREQ_COMPARE_MEMBER = FIX_TIME
XERO_FREQ_SEND_NOTIFICATION = FIX_TIME
FLARM_FREQ_UPDATE_TODAY = PER_MINUTE
FLARM_FREQ_UPDATE_FROM_LAST_TIMESTAMP = PER_DAY

CRONJOBS = [
    # A field may be an asterisk (*), which always stands for "first-last".

    # Ranges of numbers are allowed.  Ranges are two numbers separated with a
    # hyphen.  The specified range is inclusive.  For example,  8-11  for  an
    # "hours" entry specifies execution at hours 8, 9, 10 and 11.

    # Lists are allowed.  A list is a set of numbers (or ranges) separated by
    # commas.  Examples: "1,2,5,9", "0-4,8-12".

    # Step values can be used in conjunction with ranges.  Following a  range
    # with  "<number>"  specifies  skips  of  the  number's value through the
    # range.  For example, "0-23/2" can be used in the hours field to specify
    # command  execution every other hour (the alternative in the V7 standard
    # is "0,2,4,6,8,10,12,14,16,18,20,22").  Steps are also  permitted  after
    # an asterisk, so if you want to say "every two hours", just use "*/2".

    # For example,
    # "30 4 1,15 * 5" would cause a command to be run at 4:30 am on  the  1st
    # and 15th of each month, plus every Friday.
    # everyday at 17:00, execute xero 
    (XERO_FREQ_UPDATE_CONTACTS, 'xero.cron.update_contacts'),
    (XERO_FREQ_UPDATE_ITEMCODES, 'xero.cron.update_itemcodes'),
    (XERO_FREQ_SEND_NOTIFICATION, 'xero.cron.send_notification'),
    (XERO_FREQ_COMPARE_MEMBER, 'xero.cron.compare_memeber'),
    (FLARM_FREQ_UPDATE_TODAY, 'flarm.cron.update_flarm'),
    (FLARM_FREQ_UPDATE_FROM_LAST_TIMESTAMP, 'flarm.cron.update_flarm_all'),
]
