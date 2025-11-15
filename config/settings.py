"""
Django settings for mmo_board project.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third-party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'allauth.socialaccount.providers.google',
    
    # Local apps
    'accounts',
    'adverts',
    'replies',
    'newsletters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Production database (PostgreSQL)
if os.getenv('DB_NAME'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'  # обязательно со слэшем!
MEDIA_ROOT = BASE_DIR / 'media'  # папка должна существовать и быть доступной на запись

# Ограничения для медиа файлов (base64)
MAX_IMAGE_SIZE_MB = 10  # МБ для изображений
MAX_VIDEO_SIZE_MB = 100  # МБ для видео
MAX_VIDEO_DURATION = 10  # Максимальная длительность видео в секундах (не используется для base64)

# Настройки загрузки файлов для base64
FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_VIDEO_SIZE_MB * 1024 * 1024  # Размер в байтах для видео (100 МБ)
DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_VIDEO_SIZE_MB * 1024 * 1024  # Размер в байтах для данных формы

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Site ID for allauth
SITE_ID = 1

# Django Allauth settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_UNIQUE_EMAIL = True
# Используем HTTP в режиме разработки, HTTPS в production
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https' if not DEBUG else 'http'

# Email backend
# Загрузка учетных данных из файла email_credentials.txt (если существует)
email_credentials_file = BASE_DIR / 'email_credentials.txt'
if email_credentials_file.exists():
    from dotenv import dotenv_values
    email_config = dotenv_values(email_credentials_file)
    EMAIL_HOST = email_config.get('EMAIL_HOST', 'smtp.mail.ru')
    EMAIL_PORT = int(email_config.get('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = email_config.get('EMAIL_USE_TLS', 'True') == 'True'
    EMAIL_HOST_USER = email_config.get('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = email_config.get('EMAIL_HOST_PASSWORD', '')
    DEFAULT_FROM_EMAIL = email_config.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
    SERVER_EMAIL = email_config.get('SERVER_EMAIL', DEFAULT_FROM_EMAIL)
else:
    # Fallback на переменные окружения или значения по умолчанию
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.mail.ru')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'no-reply@mmo-board.local')
    SERVER_EMAIL = os.getenv('SERVER_EMAIL', DEFAULT_FROM_EMAIL)

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

# OAuth credentials
# Загрузка OAuth ключей из файла oauth_credentials.txt (если существует)
oauth_credentials_file = BASE_DIR / 'oauth_credentials.txt'
if oauth_credentials_file.exists():
    from dotenv import dotenv_values
    oauth_config = dotenv_values(oauth_credentials_file)
    
    # Yandex OAuth
    SOCIALACCOUNT_PROVIDERS = {
        'yandex': {
            'APP': {
                'client_id': oauth_config.get('YANDEX_CLIENT_ID', ''),
                'secret': oauth_config.get('YANDEX_CLIENT_SECRET', ''),
                'key': ''
            }
        },
        'google': {
            'APP': {
                'client_id': oauth_config.get('GOOGLE_CLIENT_ID', ''),
                'secret': oauth_config.get('GOOGLE_CLIENT_SECRET', ''),
                'key': ''
            },
            'SCOPE': [
                'profile',
                'email',
            ],
            'AUTH_PARAMS': {
                'access_type': 'online',
            }
        }
    }
else:
    # Fallback на переменные окружения или пустые значения
    SOCIALACCOUNT_PROVIDERS = {
        'yandex': {
            'APP': {
                'client_id': os.getenv('YANDEX_CLIENT_ID', ''),
                'secret': os.getenv('YANDEX_CLIENT_SECRET', ''),
                'key': ''
            }
        },
        'google': {
            'APP': {
                'client_id': os.getenv('GOOGLE_CLIENT_ID', ''),
                'secret': os.getenv('GOOGLE_CLIENT_SECRET', ''),
                'key': ''
            },
            'SCOPE': [
                'profile',
                'email',
            ],
            'AUTH_PARAMS': {
                'access_type': 'online',
            }
        }
    }

# Social account settings
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'mandatory'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_STORE_TOKENS = False

# Cache configuration
CACHE_BACKEND = os.getenv('CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache')

if 'DatabaseCache' in CACHE_BACKEND:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'cache_table',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'json': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
        'file_general': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'general.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'json',
            'level': 'INFO',
        },
        'file_errors': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'errors.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'json',
            'level': 'ERROR',
        },
        'file_security': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'json',
            'level': 'WARNING',
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_general'],
            'level': 'INFO',
        },
        'django.security': {
            'handlers': ['file_security', 'mail_admins'],
            'level': 'WARNING',
        },
        'accounts': {
            'handlers': ['console', 'file_general'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
        },
        'adverts': {
            'handlers': ['console', 'file_general'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
        },
        'replies': {
            'handlers': ['console', 'file_general'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
        },
        'newsletters': {
            'handlers': ['console', 'file_general'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
        },
    },
}

# Security settings (production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# APScheduler settings
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

# File upload limits
MAX_IMAGE_UPLOAD_SIZE = 15 * 1024 * 1024  # 15 MB
MAX_VIDEO_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB для видео
MAX_VIDEO_DURATION = 10  # Максимальная длительность видео в секундах

# Markdown and HTML sanitization settings
MARKDOWN_EXTENSIONS = ['fenced_code', 'tables', 'nl2br']

# Санитизация HTML (после Markdown) - настройки для bleach
BLEACH_ALLOWED_TAGS = [
    'p', 'h1', 'h2', 'h3', 'h4', 'ul', 'ol', 'li', 'a', 'img', 'blockquote', 'code', 'pre',
    'strong', 'em', 'hr', 'br', 'figure', 'figcaption', 'video', 'source'
]

BLEACH_ALLOWED_ATTRS = {
    'a': ['href', 'title', 'rel', 'target'],
    'img': ['src', 'alt', 'title', 'width', 'height', 'class', 'style'],
    'video': ['controls', 'poster', 'preload', 'width', 'height', 'class', 'style'],
    'source': ['src', 'type'],
}

BLEACH_ALLOWED_PROTOCOLS = ['http', 'https', 'mailto', 'data']  # data — если допустим data:URI для иконок

# Для обратной совместимости
ALLOWED_HTML_TAGS = BLEACH_ALLOWED_TAGS
ALLOWED_HTML_ATTRS = BLEACH_ALLOWED_ATTRS
ALLOWED_PROTOCOLS = BLEACH_ALLOWED_PROTOCOLS

# Pagination
PAGINATE_BY = 15

