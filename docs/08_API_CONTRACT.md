# Uziel OS - API Contract inicial

Base URL local:

```txt
http://localhost:8000/api
```

## 1. Health

```http
GET /api/health/
```

Respuesta:

```json
{
  "status": "ok",
  "service": "uziel-os-api"
}
```

## 2. Auth

```http
POST /api/auth/login/
POST /api/auth/logout/
POST /api/auth/refresh/
GET /api/auth/me/
```

Auth puede implementarse despues de FASE 0.

## 3. Categorias

```http
GET /api/categories/
```

Respuesta esperada:

```json
[
  { "code": "hygiene", "name": "Higiene", "color": "#3b82f6" },
  { "code": "exercise", "name": "Ejercicio", "color": "#22c55e" },
  { "code": "focus", "name": "Foco", "color": "#8b5cf6" },
  { "code": "nutrition", "name": "Alimentacion", "color": "#f97316" },
  { "code": "sleep", "name": "Sueno", "color": "#6366f1" }
]
```

## 4. Rutinas

```http
GET /api/routines/
POST /api/routines/
GET /api/routines/{id}/
PATCH /api/routines/{id}/
DELETE /api/routines/{id}/
```

## 5. Agenda

```http
GET /api/schedule/today/
GET /api/schedule/?date=YYYY-MM-DD
```

Debe devolver ejecuciones del dia ordenadas por hora.

## 6. Ejecuciones

```http
POST /api/executions/{id}/start/
POST /api/executions/{id}/pause/
POST /api/executions/{id}/resume/
POST /api/executions/{id}/complete/
POST /api/executions/{id}/snooze/
POST /api/executions/{id}/omit/
```

Todas las acciones deben pasar por la maquina de estados del backend.

## 7. Analytics

```http
GET /api/analytics/dashboard/
GET /api/analytics/weekly/
GET /api/analytics/category/{code}/
```

## 8. Dispositivos y notificaciones

```http
POST /api/devices/register/
GET /api/devices/
PATCH /api/devices/{id}/
POST /api/notifications/test/
```

## 9. DTO inicial de RoutineExecution

```ts
export interface RoutineExecutionDTO {
  id: string;
  routine_title: string;
  category: 'hygiene' | 'exercise' | 'focus' | 'nutrition' | 'sleep';
  scheduled_start: string;
  scheduled_end: string;
  actual_start: string | null;
  actual_end: string | null;
  duration_minutes: number;
  status: 'PROGRAMMED' | 'NOTIFIED' | 'SNOOZED' | 'IN_PROGRESS' | 'PAUSED' | 'COMPLETED' | 'OMITTED' | 'EXPIRED';
  progress_percent: number;
}
```

## 10. Errores

Formato recomendado:

```json
{
  "error": {
    "code": "INVALID_STATE_TRANSITION",
    "message": "La rutina no puede pasar de COMPLETED a IN_PROGRESS."
  }
}
```
