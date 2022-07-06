from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # apps
    'map_to_db',
    'funding',
    'settings'
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

# Theme settings
JAZZMIN_SETTINGS = {
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},

        # Add Mapping model to Navbar
        {"model": "map_to_db.currencysettings"}
    ],
    "custom_css": "/css/custom.css",
    "custom_js": "/js/main.js",
    "site_brand": "Administrator Panel",
    "custom_links": {
        "funding": [{
            "name": "Funding Table", 
            "url": "/admin/funding/fundingrecord/data-points/", 
            "icon": "nav-icon fas fa-circle",
        }]
    },
}

ROOT_URLCONF = 'mapper.urls'

SITE_ID=1

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
                'settings.context_processor.counter'
            ],
        },
    },
]

WSGI_APPLICATION = 'mapper.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('NAME'),
        'USER': os.getenv('USER'),
        'PASSWORD': 'Hsbc1234!',
        'HOST': os.getenv('HOST')
    }
}

TROFI_URL=os.getenv('TROFI_URL')
TROFI_SECRET=os.getenv('TROFI_SECRET')
TROFI_DEV_URL=os.getenv('TROFI_DEV_URL')
TROFI_DEV_SECRET=os.getenv('TROFI_DEV_SECRET')
TROFI_STAGING_URL=os.getenv('TROFI_STAGING_URL')
TROFI_STAGING_SECRET=os.getenv('TROFI_STAGING_SECRET')

# Password validation

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

# static files settings
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
   os.path.join(BASE_DIR, 'mapper/static/')
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kuala_Lumpur'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
