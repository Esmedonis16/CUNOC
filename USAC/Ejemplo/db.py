import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db',
        'USER': 'postgres',
        #'PASSWORD': 'Esmeralda',
        'PASSWORD': '202001466',
        'HOST': '127.0.0.1',
        'DATABASE_PORT':'5432',
    }
}