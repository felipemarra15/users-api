import os
from pathlib import Path

# === Paths ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === Seguridad / Entorno ===
# En prod: pasá DJANGO_SECRET_KEY y DJANGO_DEBUG=False por variables de entorno
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'inseguro-dev-solo')
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# === Apps ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'usuarios',
    'corsheaders',
]

# === Middleware (sin duplicados) ===
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',  # <- solo una vez
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# === URLs / WSGI ===
ROOT_URLCONF = 'proyecto.urls'
WSGI_APPLICATION = 'proyecto.wsgi.application'

# === Templates ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # agregá rutas de templates si usás carpetas personalizadas
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

# === Base de datos ===
# En local: podés dejar estos defaults o exportar variables:
#   export DB_NAME=registrodb DB_USER=postgres DB_PASS=xxx DB_HOST=172.29.144.1 DB_PORT=5432
# En K8s: vendrán de Secrets/ConfigMaps
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'registrodb'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASS', ''),
        'HOST': os.getenv('DB_HOST', '172.29.144.1'),  # tu IP de Windows por defecto (ajustá si cambia)
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# === Validadores de contraseña ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === Internacionalización ===
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'  # si querés: 'America/Montevideo'
USE_I18N = True
USE_TZ = True

# === Archivos estáticos ===
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === CORS (frontend consumiendo tu API) ===
CORS_ALLOW_ALL_ORIGINS = True


