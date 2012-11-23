import os

DEBUG_MODE = False

if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    DEBUG_MODE = True

DEBUG = DEBUG_MODE

KNOWN_HOSTS = {
    'code': 'http://discussion-app-code-env.elasticbeanstalk.com'
}
