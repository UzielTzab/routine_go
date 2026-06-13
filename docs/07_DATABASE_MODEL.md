# Uziel OS - Modelo de datos inicial

## 1. Entidades principales

| Entidad | Proposito |
|---|---|
| `RoutineCategory` | Categorias base: higiene, ejercicio, foco, alimentacion, sueno |
| `RoutineTemplate` | Definicion reutilizable de una rutina |
| `RoutineScheduleRule` | Regla de recurrencia, hora, dias y aviso previo |
| `RoutineExecution` | Instancia concreta de una rutina en una fecha/hora |
| `Device` | Dispositivo registrado para notificaciones |
| `NotificationEvent` | Auditoria de notificaciones |
| `DailyCheckIn` | Estado subjetivo diario: energia, mood, sueno |
| `FocusSession` | Detalle de sesiones de foco |
| `SleepLog` | Registro de sueno |
| `MealLog` | Registro de comidas |
| `WaterLog` | Registro opcional de agua |
| `WorkoutLog` | Registro opcional de ejercicio |

## 2. Categorias

Codigos oficiales:

```txt
hygiene
exercise
focus
nutrition
sleep
```

## 3. RoutineTemplate

Campos sugeridos:

| Campo | Tipo | Nota |
|---|---|---|
| `id` | UUID | Identificador |
| `user` | FK User | Propietario |
| `category` | FK RoutineCategory | Categoria |
| `title` | string | Nombre visible |
| `instructions` | text | Pasos o notas |
| `default_duration_minutes` | int | Duracion por defecto |
| `priority` | int | Prioridad |
| `active` | bool | Activa/inactiva |
| `created_at` | datetime | Auditoria |
| `updated_at` | datetime | Auditoria |

## 4. RoutineScheduleRule

Campos sugeridos:

| Campo | Tipo | Nota |
|---|---|---|
| `id` | UUID | Identificador |
| `routine` | FK RoutineTemplate | Rutina |
| `days_of_week` | array/string | Dias activos |
| `start_time` | time | Hora programada |
| `reminder_minutes` | int | Minutos antes |
| `timezone` | string | Zona horaria |
| `auto_complete` | bool | Auto-completar si fue iniciada |
| `active` | bool | Activa/inactiva |

## 5. RoutineExecution

Campos sugeridos:

| Campo | Tipo | Nota |
|---|---|---|
| `id` | UUID | Identificador |
| `routine` | FK RoutineTemplate | Rutina origen |
| `user` | FK User | Propietario |
| `scheduled_start` | datetime | Hora planeada |
| `scheduled_end` | datetime | Fin planeado |
| `actual_start` | datetime/null | Inicio real |
| `actual_end` | datetime/null | Fin real |
| `duration_minutes` | int | Duracion |
| `status` | choice | Estado |
| `source` | choice | app, notification, system |
| `notes` | text/null | Nota opcional |
| `created_at` | datetime | Auditoria |
| `updated_at` | datetime | Auditoria |

## 6. Estados oficiales

```txt
PROGRAMMED
NOTIFIED
SNOOZED
IN_PROGRESS
PAUSED
COMPLETED
OMITTED
EXPIRED
```

## 7. Regla critica de auto-completado

No se debe marcar una rutina como `COMPLETED` si nunca paso por `IN_PROGRESS`.

Si no hay accion del usuario, el estado correcto debe ser:

- `EXPIRED`,
- `OMITTED`, o
- pendiente segun regla futura.

## 8. Indices recomendados

- `RoutineExecution(user, scheduled_start)`
- `RoutineExecution(user, status)`
- `RoutineExecution(user, scheduled_start, status)`
- `RoutineTemplate(user, category, active)`
- `NotificationEvent(execution, type, status)`
- `Device(user, platform, push_enabled)`
