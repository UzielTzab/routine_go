# Uziel OS - Variables de entorno

## 1. Regla principal

Nunca subir `.env` reales a GitHub.

Si una variable es necesaria, debe documentarse en `.env.example`.

## 2. Backend `.env.example`

Ubicacion:

```txt
backend/.env.example
```

Contenido recomendado:

```env
DJANGO_SECRET_KEY=change-me-local-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,backend
DJANGO_SETTINGS_MODULE=config.settings.local

POSTGRES_DB=uziel_os
POSTGRES_USER=uziel_os_user
POSTGRES_PASSWORD=uziel_os_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgres://uziel_os_user:uziel_os_password@db:5432/uziel_os

REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1

CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

TIME_ZONE=America/Merida
LANGUAGE_CODE=es-mx
```

## 3. Frontend `.env.example`

Ubicacion:

```txt
frontend/.env.example
```

Contenido recomendado:

```env
VITE_APP_NAME=Uziel OS
VITE_API_BASE_URL=http://localhost:8000/api
VITE_ENABLE_MOCKS=false
VITE_DEFAULT_LOCALE=es-MX
VITE_DEFAULT_TIMEZONE=America/Merida
```

## 4. Raiz `.env.example`

Opcional para Docker Compose si se decide centralizar variables:

```env
COMPOSE_PROJECT_NAME=uziel_os
POSTGRES_DB=uziel_os
POSTGRES_USER=uziel_os_user
POSTGRES_PASSWORD=uziel_os_password
POSTGRES_PORT=5432
BACKEND_PORT=8000
REDIS_PORT=6379
```

## 5. Variables futuras

Para notificaciones:

```env
VAPID_PUBLIC_KEY=
VAPID_PRIVATE_KEY=
FCM_SERVER_KEY=
```

Para produccion:

```env
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=api.tudominio.com
DATABASE_URL=postgres://...
REDIS_URL=redis://...
```

## 6. Seguridad

- `.env` debe estar en `.gitignore`.
- `.env.example` si se versiona.
- No imprimir secretos en logs.
- No poner claves en README.
