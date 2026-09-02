"""
Django settings for Gen-Z Constructors Limited Company project.
Ready for production deployment on HostNali shared hosting (/home2/genzcons).
"""

from pathlib import Path
import os
import sys
from dotenv import load_dotenv
from django.templatetags.static import static
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-genz-constructors-production-secret-key-change-in-prod-2026'
)

# DEBUG is True only if explicitly set to 'true' in .env
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv(
        'ALLOWED_HOSTS',
        'localhost,127.0.0.1,genzconstructors.co.ke,www.genzconstructors.co.ke'
    ).split(',')
    if h.strip()
]

# CSRF Trusted Origins for HTTPS
csrf_origins_env = os.getenv(
    'CSRF_TRUSTED_ORIGINS',
    'genzconstructors.co.ke,www.genzconstructors.co.ke,127.0.0.1,localhost'
)
CSRF_TRUSTED_ORIGINS = [
    f"https://{h.strip()}" if not h.strip().startswith(('http://', 'https://')) else h.strip()
    for h in csrf_origins_env.split(',')
    if h.strip()
]

# Application definition - Note: 'unfold' must be placed before 'django.contrib.admin'
INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    # Custom apps
    'core.apps.CoreConfig',
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
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                # Core custom context processor
                'core.context_processors.site_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# ==============================================================================
# DATABASE CONFIGURATION (Supports MySQL, PostgreSQL, SQLite on Shared Hosting)
# ==============================================================================
db_engine = os.getenv('DB_ENGINE', '').strip()
if db_engine:
    DATABASES = {
        'default': {
            'ENGINE': db_engine,
            'NAME': os.getenv('DB_NAME', 'genzcons_db'),
            'USER': os.getenv('DB_USER', 'genzcons_user'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '3306' if 'mysql' in db_engine else '5432'),
            'OPTIONS': {
                'charset': 'utf8mb4',
            } if 'mysql' in db_engine else {},
        }
    }
else:
    # Default to SQLite for local development or simple shared hosting
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ==============================================================================
# CACHE CONFIGURATION (Database Cache for shared hosting performance)
# ==============================================================================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'genz_cache_table',
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
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Max upload size: 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# PRODUCTION SECURITY HEADERS & SSL PROXY
# ==============================================================================
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# ==============================================================================
# DJANGO UNFOLD CONFIGURATION & THEME CUSTOMIZATION
# ==============================================================================
UNFOLD = {
    "SITE_TITLE": "Gen-Z Constructors Administration",
    "SITE_HEADER": "Gen-Z Constructors",
    "SITE_SUBHEADER": "Building Your Vision, Constructing Your Future",
    "SITE_ICON": {
        "light": lambda request: static("images/logo.jpg"),
        "dark": lambda request: static("images/logo.jpg"),
    },
    "SITE_LOGO": {
        "light": lambda request: static("images/logo.jpg"),
        "dark": lambda request: static("images/logo.jpg"),
    },
    "SITE_SYMBOL": "speed",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "LOGIN": {
        "image": lambda request: static("images/logo.jpg"),
        "redirect_after": lambda request: reverse_lazy("admin:index"),
    },
    "STYLES": [
        lambda request: static("css/unfold_custom.css"),
    ],
    "COLORS": {
        "primary": {
            "50": "241 237 223",   # Warm Ivory (#F1EDDF)
            "100": "237 218 160",  # Light Champagne Gold (#EDDAA0)
            "200": "220 190 115",
            "300": "200 165 85",
            "400": "185 143 61",   # Rich Construction Gold (#B98F3D)
            "500": "165 125 45",
            "600": "137 99 33",    # Bronze Gold (#896321)
            "700": "66 51 30",     # Dark Bronze (#42331E)
            "800": "8 6 10",       # Deep Black (#08060A)
            "900": "1 11 32",      # Midnight Navy (#010B20)
            "950": "1 8 24",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Navigation & Overview",
                "separator": True,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": "View Live Website",
                        "icon": "public",
                        "link": "/",
                    },
                ],
            },
            {
                "title": "Business Content",
                "separator": True,
                "items": [
                    {
                        "title": "Site Settings",
                        "icon": "tune",
                        "link": reverse_lazy("admin:core_sitesettings_changelist"),
                    },
                    {
                        "title": "Services & Solutions",
                        "icon": "construction",
                        "link": reverse_lazy("admin:core_service_changelist"),
                    },
                    {
                        "title": "Projects Portfolio",
                        "icon": "apartment",
                        "link": reverse_lazy("admin:core_project_changelist"),
                    },
                    {
                        "title": "7-Step Process",
                        "icon": "timeline",
                        "link": reverse_lazy("admin:core_processstep_changelist"),
                    },
                    {
                        "title": "Testimonials",
                        "icon": "star",
                        "link": reverse_lazy("admin:core_testimonial_changelist"),
                    },
                    {
                        "title": "FAQs",
                        "icon": "quiz",
                        "link": reverse_lazy("admin:core_faq_changelist"),
                    },
                ],
            },
            {
                "title": "Leads & Inquiries",
                "separator": True,
                "items": [
                    {
                        "title": "Project Quotes & Enquiries",
                        "icon": "request_quote",
                        "link": reverse_lazy("admin:core_enquiry_changelist"),
                    },
                    {
                        "title": "Contact Messages",
                        "icon": "mark_email_unread",
                        "link": reverse_lazy("admin:core_contactmessage_changelist"),
                    },
                ],
            },
        ],
    },
}

# ==============================================================================
# SMTP EMAIL CONFIGURATION (Latest Free Django SMTP Backend / Gmail App Password)
# ==============================================================================
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False').lower() in ('true', '1', 'yes')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'genzconstructors@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')  # Standard password or 16-char Gmail App Password
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'Gen-Z Constructors <genzconstructors@gmail.com>')

# Company Information Fallbacks
COMPANY_NAME = "Gen-Z Constructors Limited Company"
COMPANY_PHONE = os.getenv('COMPANY_PHONE', '+254713706103')
COMPANY_WHATSAPP = os.getenv('COMPANY_WHATSAPP', '254713706103')
COMPANY_EMAIL = os.getenv('COMPANY_EMAIL', 'genzconstructors@gmail.com')
COMPANY_DOMAIN = os.getenv('COMPANY_DOMAIN', 'genzconstructors.co.ke')
