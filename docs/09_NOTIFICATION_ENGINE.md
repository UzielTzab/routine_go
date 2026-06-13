# Uziel OS - Notification Engine

## 1. Objetivo

Enviar recordatorios antes de cada rutina, permitir acciones rapidas y actualizar el estado de ejecuciones.

## 2. Estrategia por capas

| Capa | Uso |
|---|---|
| Backend | Fuente de verdad, agenda, estados, eventos y Celery |
| Redis | Broker de tareas y soporte para procesos asincronos |
| Celery Beat | Detecta ejecuciones proximas y vencimientos |
| Celery Worker | Ejecuta envio de notificaciones y auto-completado |
| PWA Service Worker | Recibe Web Push y maneja acciones web |
| Capacitor | Notificaciones locales moviles confiables en fase posterior |

## 3. Dependencia de Redis

Redis forma parte del entorno base desde FASE 0 porque sera necesario para:

- detectar rutinas proximas,
- enviar notificaciones previas,
- registrar eventos,
- completar rutinas iniciadas,
- procesar reportes,
- preparar tareas programadas.

En FASE 0 solo debe quedar disponible. La logica final se implementa en fases posteriores.

## 4. Flujo tecnico de notificacion

1. `Celery Beat` revisa ejecuciones proximas.
2. `NotificationSchedulerService` decide si corresponde notificar.
3. Se crea `NotificationEvent`.
4. `NotificationDispatchService` envia la notificacion.
5. El usuario toca `Iniciar`, `Posponer` u `Omitir`.
6. El handler llama al endpoint correspondiente.
7. `ExecutionStateMachine` valida la transicion.
8. El dashboard se actualiza.

## 5. Acciones

Acciones deseadas:

- `start`: iniciar rutina.
- `snooze`: posponer.
- `omit`: omitir.
- `open`: abrir detalle.

## 6. Fallback obligatorio

No todos los navegadores/sistemas operativos muestran botones en notificaciones.

Si no hay acciones, tocar la notificacion debe abrir:

```txt
/executions/{id}
```

o la pantalla equivalente de la rutina activa.

## 7. Regla de auto-completado

No auto-completar rutinas no iniciadas.

Valido:

```txt
NOTIFIED -> IN_PROGRESS -> COMPLETED
```

Invalido:

```txt
NOTIFIED -> COMPLETED
```

salvo accion manual explicita del usuario.

## 8. Estados relacionados

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

## 9. Payload sugerido

```json
{
  "execution_id": "uuid",
  "title": "Lavarse el rostro y yoga facial",
  "category": "hygiene",
  "scheduled_start": "2026-01-01T07:00:00-06:00",
  "duration_minutes": 30,
  "actions": ["start", "snooze", "omit"]
}
```

## 10. Fases

| Fase | Entregable |
|---|---|
| FASE 0 | Redis disponible en Docker |
| FASE 3 | Modelos de rutinas y ejecuciones |
| FASE 5 | Maquina de estados |
| FASE 7 | Notificaciones PWA |
| FASE 8 | Capacitor y notificaciones locales |
