from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG') == 'True'

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'st-peter-lib.onrender.com',
    '52.45.145.20',
    'stpeterlibrary.crabdance.com',
]


# Application definition

INSTALLED_APPS = [
    #My_apps
    'books',
    'posts',
    'my_auth',
    'api',
    #django rest framework
    'rest_framework',
    'rest_framework.authtoken',
    #django rest authentication
    'dj_rest_auth',
    #CORS headers for APIs
    "corsheaders",
    #django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    #whitenoise static
    "whitenoise.runserver_nostatic",
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #CORS headers middleware
    "corsheaders.middleware.CorsMiddleware",
    #whitenoise
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'library.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates/'],
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

WSGI_APPLICATION = 'library.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static/',
]
#Static ROOT
STATIC_ROOT = BASE_DIR / 'staticfiles'

#Whitenoise storage
STORAGES = {
    # ...
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
        'OPTIONS': {
            'location': BASE_DIR / 'media/',
        },
        'PREFIX': '/media/',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

#Media settings

MEDIA_ROOT = BASE_DIR / 'media/'
MEDIA_URL = '/media/'

#Rest API pagination settings

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
    'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework.authentication.TokenAuthentication',
       'rest_framework.authentication.SessionAuthentication'
   ),
}

FIXTURES_DIRS = [
    BASE_DIR / 'fixtures',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#CSRF Setting
CSRF_TRUSTED_ORIGINS = [
    'https://st-peter-lib.onrender.com',
    'http://52.45.145.20',
    'http://stpeterlibrary.crabdance.com/',
]

#CORS Settings
CORS_ALLOWED_ORIGINS = [
    'https://stpeterlibrary.flutterflow.app',
    'http://localhost:8080',
    'http://52.45.145.20',
    'http://stpeterlibrary.crabdance.com',
]