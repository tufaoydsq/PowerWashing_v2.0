import os
from pathlib import Path
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
import django_heroku
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==================================================================
# SEGURANÇA
# ==================================================================
# SECURITY WARNING: nunca deixar a secret key em texto simples no código.
# Definir SECRET_KEY como variável de ambiente no Railway (ou onde fizeres deploy).
# Localmente, cria um ficheiro .env (NÃO subir para o git) ou exporta no terminal.
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-!)kk^js_66cyvlsn4dog9-4amy%il#u8l+wnju5ec9kdpy8v&^'  # usado só se não houver env var (dev local)
)

# SECURITY WARNING: don't run with debug turned on in production!
# Por padrão False; só fica True se definires DEBUG=True no ambiente local.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    "lavandaria-production.up.railway.app",
    "laudrybox.up.railway.app",
    "localhost",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
    "https://lavandaria-production.up.railway.app",
    "https://laudrybox.up.railway.app"
]


# Application definition

INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used


    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "core.apps.CoreConfig",
    "crm.apps.CrmConfig",

    'import_export',
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

ROOT_URLCONF = 'powerWashing.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' /'templates']
        ,
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

WSGI_APPLICATION = 'powerWashing.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# POSTGRES_LOCALLY =False
# if not DEBUG or POSTGRES_LOCALLY:
#     DATABASES['default'] = dj_database_url.parse(os.environ.get('DATABASE_URL', ''))

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'yuransnts@gmail.com')
# SECURITY WARNING: nunca deixar a senha/app-password em texto simples.
# Definir EMAIL_HOST_PASSWORD como variável de ambiente.
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = 'Power Washing <yuransnts@gmail.com>'
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


# ==================================================================
# SESSÃO / LOGOUT AUTOMÁTICO
# ==================================================================
# Antes: nenhuma destas estava definida -> Django usava o padrão de
# 2 semanas (1209600s) e a sessão sobrevivia ao fechar o navegador.
#
# Agora: logout automático após 30 minutos de INATIVIDADE (não um
# tempo fixo desde o login) - mais apropriado para um sistema com
# faturas, pagamentos e cobrança de licenças.
SESSION_COOKIE_AGE = 1800            # 30 minutos, em segundos
SESSION_SAVE_EVERY_REQUEST = True    # renova o tempo a cada pedido -> mede inatividade
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # fecha a sessão ao fechar o navegador

# Extra: cookies de sessão só via HTTPS em produção
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Maputo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = '/images/service/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
MEDIA_ROOT = BASE_DIR / 'static/images/service'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
django_heroku.settings(locals())

UNFOLD = {
    "SITE_TITLE": "LaundryBox",

    "SITE_URL": "/",
    "SITE_LOGO": {
        "light": lambda request: static("img/local/icon.png"),  # light mode
        "dark": lambda request: static("img/local/icon.png"),  # dark mode
    },
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x24",
            "type": "image/svg+xml",
            "href": lambda request: static("img/local/logo.jpg"),
        },
    ],
    "SHOW_HISTORY": True, # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": False, # show/hide "View on site" button, default: True
    "DASHBOARD_CALLBACK": "core.views.dashboard_callback",

    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "separator": False,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                    },
                

                ],
            },
            {
                "title": _("View applications"),
                "separator": False,
                "collapsible": False,
                "items": [

                    {
                        "title": _("Lavandaria"),
                        "icon": "store",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:core_lavandaria_changelist"),  # Link para a lista de Suppliers
                        "permission": lambda request: request.user.has_perm("core.view_lavandaria"),
                    },
                    {
                        "title": _("Staff"),
                        "icon": "person",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:core_funcionario_changelist"),  # Link para a lista de Suppliers
                        "permission": lambda request: request.user.has_perm("core.view_funcionario"),
                    },
                    {
                        "title": _("Artigos"),
                        "icon": "dry_cleaning",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:core_itemservico_changelist"),  # Link para a lista de Customers
                        "permission": lambda request: request.user.has_perm("core.view_itemservico"),
                    },
                    {
                        "title": _("Clientes"),
                        "icon": "handshake",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:core_cliente_changelist"),  # Link para a lista de Customers
                        "permission": lambda request: request.user.has_perm("core.view_cliente"),
                    },
                    {
                        "title": _("Pedidos"),
                        "icon": "shopping_cart",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:core_pedido_changelist"),  # Link para a lista de Customers
                        "permission": lambda request: request.user.has_perm("core.view_pedido"),
                    },
                                        {
                        "title": _("Recibos"),
                        "icon": "receipt_long",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:core_recibo_changelist"),  # Link para a lista de Customers
                        "permission": lambda request: request.user.has_perm("core.view_recibo"),
                    },

                ]
            }
        ],
    },


}
