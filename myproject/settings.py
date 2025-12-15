# myproject/settings.py

from pathlib import Path
import os
import dj_database_url
# The 'dj_database_url' package is used to parse the PostgreSQL URL for deployment.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
# 1. CRITICAL CHANGE: Load SECRET_KEY from environment variables for security.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-t2h5a6_u$*7i2%7w2v-k9x1=r1y#x&s^8@o=c!^x3x1#')

# SECURITY WARNING: don't run with debug turned on in production!
# 2. CRITICAL CHANGE: Set to False for the live server!
DEBUG = os.environ.get('DEBUG') == 'True'

# 3. CRITICAL CHANGE: The live server domain must be included here.
# We include the Render/Railway defaults and load from environment for flexibility.
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', os.environ.get('ALLOWED_HOSTS', '')]
# Filter out empty strings if multiple hosts are specified
ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS if h.strip()]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'portal',
    'widget_tweaks',
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

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# 4. CRITICAL CHANGE: Use environment variable 'DATABASE_URL' for production (PostgreSQL).
# Fallback to local SQLite for development if DATABASE_URL is not set.

if 'DATABASE_URL' in os.environ:
    # Production Database (PostgreSQL)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
    
    # Optional: Force SSL connections for security if the database URL specifies it
    # DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}

else:
    # Local Development Database (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


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


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# 5. CRITICAL CHANGE: Static file configuration for production

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles_build' # Location for collectstatic to dump files

# Tell Django about the static files folders in each app
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Custom settings
LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'

# For security: ensure clickjacking protection is enabled
X_FRAME_OPTIONS = 'DENY'

# For brute-force protection variables in views.py (if you use them)
# LOCKOUT_TIME is defined in views.py, but you might want to adjust cache settings here
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / 'django_cache_files',
    }
}