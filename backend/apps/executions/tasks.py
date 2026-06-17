from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from apps.executions.models import RoutineExecution
from apps.executions.services.state_machine import ExecutionStateMachineService
from apps.notifications.models import Notification

GRACE_PERIOD_MINUTES = 15
REMINDER_MINUTES = 10 # Se enviará la notificación cuando la tarea vaya a empezar en N minutos (si rule.reminder_minutes no existiera)

@shared_task
def check_expired_executions_task():
    """
    Tarea cron que pasa ejecuciones atrasadas a estado OMITTED.
    Utiliza un Grace Period de 15 minutos.
    """
    now = timezone.now()
    threshold_time = now - timedelta(minutes=GRACE_PERIOD_MINUTES)
    
    expired_executions = RoutineExecution.objects.filter(
        status__in=['PENDING', 'IN_PROGRESS'],
        scheduled_end__lt=threshold_time
    ).select_related('routine')

    count = 0
    for execution in expired_executions:
        try:
            # Check if any rule has auto_complete=True
            is_auto_complete = False
            rules = execution.routine.schedule_rules.all()
            for r in rules:
                if r.auto_complete:
                    is_auto_complete = True
                    break

            if is_auto_complete and execution.status == 'IN_PROGRESS':
                ExecutionStateMachineService.complete(execution)
                if execution.notes:
                    execution.notes += "\nMarcada como completada automáticamente por auto-completado."
                else:
                    execution.notes = "Marcada como completada automáticamente por auto-completado."
                execution.save(update_fields=['notes'])
            else:
                ExecutionStateMachineService.omit(execution)
                if execution.notes:
                    execution.notes += f"\nMarcada como omitida automáticamente por vencimiento (límite superado en más de {GRACE_PERIOD_MINUTES} min)."
                else:
                    execution.notes = f"Marcada como omitida automáticamente por vencimiento (límite superado en más de {GRACE_PERIOD_MINUTES} min)."
                execution.save(update_fields=['notes'])
            count += 1
        except Exception as e:
            # En producción, se logearía el error e intentaría continuar
            print(f"Error procesando execution {execution.id}: {str(e)}")
            
    return f"{count} ejecuciones procesadas (completadas u omitidas)."

import json
from pywebpush import webpush, WebPushException
from django.conf import settings
from apps.notifications.models import Notification, PushSubscription

@shared_task
def prepare_upcoming_notifications_task():
    """
    Detecta rutinas por comenzar y crea una Notificación si no ha sido enviada.
    """
    now = timezone.now()
    # Ventana desde ahora hasta dentro de REMINDER_MINUTES
    upcoming_time = now + timedelta(minutes=REMINDER_MINUTES)
    
    upcoming_executions = RoutineExecution.objects.filter(
        status='PENDING',
        notification_sent=False,
        scheduled_start__lte=upcoming_time,
        scheduled_start__gte=now # Evitar notificar tareas pasadas
    ).select_related('user', 'routine')

    count = 0
    notifications_to_create = []
    executions_to_update = []
    
    for execution in upcoming_executions:
        notif = Notification(
            user=execution.user,
            execution=execution,
            title=f"¡Tu rutina '{execution.routine.title}' está por comenzar!",
            message=f"Prepárate. Tienes agendada esta rutina para las {execution.scheduled_start.strftime('%H:%M')}."
        )
        notifications_to_create.append(notif)
        execution.notification_sent = True
        executions_to_update.append(execution)
        count += 1
        
        # Enviar Web Push a todas las suscripciones del usuario
        payload = json.dumps({
            "title": notif.title,
            "body": notif.message,
            "data": {
                "execution_id": str(execution.id)
            },
            "actions": [
                {"action": "start", "title": "Iniciar"}
            ]
        })
        
        subscriptions = PushSubscription.objects.filter(user=execution.user)
        for sub in subscriptions:
            try:
                webpush(
                    subscription_info={
                        "endpoint": sub.endpoint,
                        "keys": {
                            "p256dh": sub.p256dh,
                            "auth": sub.auth
                        }
                    },
                    data=payload,
                    vapid_private_key=settings.VAPID_PRIVATE_KEY,
                    vapid_claims={
                        "sub": settings.VAPID_ADMIN_EMAIL
                    }
                )
            except WebPushException as ex:
                if ex.response is not None and ex.response.status_code in [404, 410]:
                    # Suscripción caducada o inválida, se elimina
                    sub.delete()
                else:
                    print(f"Error enviando push a {sub.user.username}: {ex}")

    if count > 0:
        Notification.objects.bulk_create(notifications_to_create)
        RoutineExecution.objects.bulk_update(executions_to_update, ['notification_sent'])

    return f"{count} notificaciones preparadas y enviadas."
