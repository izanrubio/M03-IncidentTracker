"""
settings_ci.py – Configuració lleugera per al CI de Jenkins.
Usa SQLite en memòria → no cal cap servidor PostgreSQL extern.
"""
from .settings import *  # hereta tota la configuració base

# ── Base de dades: SQLite en memòria ──────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# ── Desactiva el sistema de caché per simplificar ─────────────────────────────
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# ── Contrasenya simple per als tests (més ràpid) ──────────────────────────────
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
