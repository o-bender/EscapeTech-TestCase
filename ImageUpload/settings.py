import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTH_USER_MODEL = 'main.User'
INSTALLED_APPS = [
    'TestCase',
    'ImageUpload',
]
SECRET_KEY = 'testsetssfdfsdfsdrf23r2f'
REDIS_HOST = 'localhost'
REDIS_PORT = '7777'
BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}