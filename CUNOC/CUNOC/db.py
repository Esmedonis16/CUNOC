import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'CUNOC',
        'USER': 'postgres',
        'PASSWORD': 'Esmeralda',
        'HOST': '127.0.0.1',
        'DATABASE_PORT':'5432',
    }
}