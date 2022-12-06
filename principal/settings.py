import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+4)%8jk1j*&hozv$vp(-c)(c(4%dr3b#yig7zcbh96gqj-vydc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'rfid.apps.RfidConfig',
    'rest_api.apps.RestApiConfig',
    'django_tables2',
    'django_extensions',
    'widget_tweaks'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'principal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'principal.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if os.getenv('GAE_APPLICATION', None) or os.getenv('GAE_INSTANCE', None):
    # Running on production App Engine, so connect to Google Cloud SQL using
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': '/cloudsql/healthy-zone-266815:us-central1:iot-rfid-test',
            'PORT': '5432',
            'NAME': 'iot-demo',
            'USER': 'iot_app_user',
            'PASSWORD': 'tkGcbOC2w8x3tos1',
        }
    }
elif os.getenv('BD_DEBUG'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'iotdemo',
            'USER': 'iot',
            'PASSWORD': 'iot_password',
            'HOST': 'localhost',
            'PORT': '5432'
        }
    }
else:
    # Running locally so connect to either a local MySQL instance or connect
    # to Cloud SQL via the proxy.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': os.getenv('DATABASE_HOST', 'localhost'),
            'PORT': '5432',
            'NAME': os.getenv('DATABASE_NAME', 'logistic'),
            'USER': os.getenv('DATABASE_USER', 'logistic'),
            'PASSWORD': os.getenv('DATABASE_PASSWORD', 'logistic')
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es-CO'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# STATIC_ROOT  = "static"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Media Files, and user uploads

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "/media/"

# RFID Reading cycle
# Defines the  interval de reader is updating data in minutes
RFID_READING_CYCLE = 5
