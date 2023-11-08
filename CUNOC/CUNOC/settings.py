"""
Django settings for Xela project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

import CUNOC.db as db

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gra*8lnioqc^p377uzxyy6=#*k8@teu6a&cjn9mjws$ss0&+(c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #MyApps
    'contraseña_olvidada',
    'Admin_y_Docentes',
    'ESTUDIANTES', 
    'profiles', 
    'logs', 

    #Third Apps
    'crispy_forms',
    'axes',
    'crispy_bootstrap4',


]

X_FRAME_OPTION = 'SAMEORIGIN'

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-info",
    "accent": "accent-navy",
    "navbar": "navbar-cyan navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-info",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "materia",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": False

}



JAZZMIN_SETTINGS = {
    
    "show_ui_builder": True,
    "site_title": "CUNOC-USAC",
    "site_header": "Administración USAC",
    "site_brand": "CUNOC",
    "site_logo": "img/logocunoc.jpg",
    "login_logo": "img/CUNOC.png",
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "user_avatar": "img/logocunoc.jpg",
    "custom_css": "static/css/custom.css",
    "welcome_sign": "Bienvenidos al Panel de Administración y Docentes",
    
    "icons": {
        "auth": "fas fa-users",
        "Admin_y_Docentes.cursos": "fas fa-solid fa-laptop",
        "Admin_y_Docentes.inges": "fas fa-users",
        "Admin_y_Docentes.notas": "fas fa-solid fa-file",
        "Admin_y_Docentes.registros": "fas fa-solid fa-id-card",
        "": "",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    
    # Use modals instead of popups
    "related_modal_active": False,
    
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    # Add a language dropdown into the admin
    
    

}

AUTHENTICATION_BACKENDS = [
    # AxesStandaloneBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesStandaloneBackend',

    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'CUNOC.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'Templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'CUNOC.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = db.POSTGRESQL


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'ESTUDIANTES.password_validators.UppercaseValidator',
    },
    {
        'NAME': 'ESTUDIANTES.password_validators.DigitValidator',
    },
    {
        'NAME': 'ESTUDIANTES.password_validators.SymbolValidator',
    },

]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'es-eu'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    # os.path.join(BASE_DIR, 'users_pictures'),
]


# Emails
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS=True #seguridad de transporte
EMAIL_PORT = 587
EMAIL_HOST_USER = "academiacunoc@gmail.com"
EMAIL_HOST_PASSWORD = "jyjt qwnt ssop tuda"


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

AXES_FAILURE_LIMIT = 3
AXES_COOLOFF_TIME = 2
AXES_LOCKOUT_CALLABLE = "ESTUDIANTES.views.lockout"
AXES_ONLY_USER_FAILURES = True


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Si quieres que la sesión persista incluso después de cerrar el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# Tiempo que la sesión estará activa, en segundos (esto es igual a 2 semanas)
SESSION_COOKIE_AGE = 1209600


LOGIN_URL = '/LoginEstudiantes/'
LOGIN_REDIRECT_URL = '/home/'
