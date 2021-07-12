import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','avishekdjangoblog.herokuapp.com']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',

    'django.contrib.humanize',
    'django.contrib.postgres',
    
    'ckeditor',
    'ckeditor_uploader',
    'django_social_share',
    'admin_honeypot',
    'hitcount',


    'posts.apps.PostsConfig',
    'accounts.apps.AccountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

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
                'posts.context_processor.categories',
                'accounts.views.site_user',
                'posts.context_processor.sidebar_posts',
                'posts.context_processor.sidebar_comments',
                'posts.context_processor.subscribe_form',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'


DATABASES = {}

DATABASES['default'] = dj_database_url.config(conn_max_age=600)


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'

MEDIA_URL = '/blog_media/'

CKEDITOR_UPLOAD_PATH = "uploads/"

MEDIA_ROOT = BASE_DIR / 'blog_media'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR/'static'
]

# LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'posts:all-posts'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'basic',
        'height': 725,
        'width': 'auto',
        'extraPlugins': 'wordcount',
        'wordcount': {
            'showParagraphs': True,
            'showWordCount': True,
            'showCharCount': True,
            'countSpacesAsChars': False,
            'countHTML': False,
            'maxWordCount': -1,
            'maxCharCount': 2000
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUD_NAME'),
    'API_KEY': os.environ.get('API_KEY'),
    'API_SECRET': os.environ.get('API_SECRET')
}


if os.getcwd() == '/app':
    DEBUG = False

    
