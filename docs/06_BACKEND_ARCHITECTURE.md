# Uziel OS - Backend Architecture

## 1. Stack backend

- Python
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Celery Beat
- Docker Compose
- django-cors-headers
- dj-database-url o django-environ

## 2. Principio tecnico

El backend es la fuente de verdad. El frontend no decide reglas criticas.

El backend controla:

- Usuarios y permisos.
- Rutinas.
- Agenda.
- Ejecuciones.
- Transiciones de estado.
- Auto-completado.
- Notificaciones.
- Metricas y analytics.

## 3. Arquitectura dockerizada

Desde FASE 0, el backend debe ejecutarse con Docker Compose.

Servicios esperados:

| Servicio | Responsabilidad |
|---|---|
| `backend` | API Django REST Framework |
| `db` | PostgreSQL para datos persistentes |
| `redis` | Broker/cache para Celery y futuras notificaciones |
| `celery_worker` | Tareas asincronas |
| `celery_beat` | Tareas programadas |

## 4. Estructura backend

```txt
backend/
├── apps/
│   ├── accounts/
│   ├── analytics/
│   ├── common/
│   ├── executions/
│   ├── notifications/
│   ├── routines/
│   ├── schedule/
│   ├── focus/
│   ├── nutrition/
│   ├── sleep/
│   ├── exercise/
│   └── hygiene/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── celery.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── Dockerfile
├── .dockerignore
├── entrypoint.sh
├── .env.example
├── requirements.txt
└── manage.py
```

## 5. Apps Django

| App | Responsabilidad |
|---|---|
| `accounts` | Usuarios, perfil, preferencias |
| `routines` | Plantillas y reglas recurrentes |
| `schedule` | Agenda diaria y planificacion |
| `executions` | Instancias, estados y maquina de estados |
| `notifications` | Dispositivos, tokens, eventos y envios |
| `analytics` | Metricas, rachas, reportes y dashboard |
| `focus` | Sesiones de foco y distracciones |
| `nutrition` | Comidas, agua y registros simples |
| `sleep` | Sueno y calidad percibida |
| `exercise` | Actividad fisica |
| `hygiene` | Rutinas de higiene |
| `common` | Utilidades compartidas |

## 6. Servicios de dominio

Crear servicios para reglas importantes:

```txt
apps/executions/services/state_machine.py
apps/schedule/services/planner.py
apps/notifications/services/scheduler.py
apps/notifications/services/dispatch.py
apps/executions/services/auto_completion.py
apps/analytics/services/dashboard.py
```

## 7. Reglas de views

Las views y ViewSets deben ser delgadas.

Permitido:

- Validar serializer.
- Llamar servicio.
- Devolver response.

No permitido:

- Calcular reglas de negocio complejas.
- Cambiar estados manualmente sin StateMachine.
- Mezclar queries, validaciones y efectos secundarios en una view gigante.

## 8. Base de datos

La base oficial de desarrollo es PostgreSQL en Docker.

SQLite no debe ser la base principal. Solo podria usarse para pruebas aisladas si el equipo lo decide explicitamente.

## 9. Redis

Redis es parte del entorno base porque se usara para:

- Celery broker.
- Result backend opcional.
- Tareas de notificaciones.
- Auto-completado.
- Futuro cache.

## 10. Health Check

Endpoint obligatorio:

```txt
GET /api/health/
```

Respuesta:

```json
{
  "status": "ok",
  "service": "uziel-os-api"
}
```

## 11. Docker Compose esperado

Debe existir `docker-compose.yml` en la raiz con:

- `backend`
- `db`
- `redis`
- `celery_worker` preparado
- `celery_beat` preparado

## 12. Buenas practicas

- Settings por ambiente.
- Variables desde `.env`.
- Serializers separados cuando aplique.
- Permisos por usuario.
- Transacciones atomicas en cambios de estado.
- Indices en `user`, `scheduled_start`, `status`, `category`.
- Tareas Celery idempotentes.
- Logs estructurados.
