import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = BASE_DIR / '.env'
if not dotenv_path.exists():
    dotenv_path = BASE_DIR / 'Toolson' / '.env'
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-only")
DEBUG = os.environ.get("DEBUG", "False") == "True"
GOOGLE_OAUTH_CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".onrender.com"
]

# -------------------
# INSTALLED APPS
# -------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'Grinding.apps.GrindingConfig',
    'sass_processor',
]

# -------------------
# MIDDLEWARE (CRITICAL ORDER)
# -------------------
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

# -------------------
# TEMPLATES
# -------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'template',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -------------------
# DATABASE
# -------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -------------------
# STATIC FILES (PRODUCTION READY)
# -------------------
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'Toolson' / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# -------------------
# SECURITY
# -------------------
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'index'

# Django requires this setting to be present; it points to this project's URLconf.
ROOT_URLCONF = 'Toolson.urls'
