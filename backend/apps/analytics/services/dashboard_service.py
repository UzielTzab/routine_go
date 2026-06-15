from django.utils import timezone
from datetime import timedelta
from apps.executions.models import RoutineExecution
from apps.routines.models import Category
from apps.schedule.services.agenda_service import get_today_agenda

class DashboardService:
    @staticmethod
    def get_current_streak(user) -> int:
        """
        Calcula el streak verificando hacia atrás desde hoy (o ayer) 
        cuántos días consecutivos tienen al menos un COMPLETED.
        """
        today = timezone.now().date()
        streak = 0
        current_date = today
        
        # Consideramos si la racha se rompió si ni hoy ni ayer hubo rutinas completadas
        # Pero simplificaremos: contamos desde hoy hacia atrás. Si hoy no hay nada, miramos ayer.
        # Si ayer no hay nada, la racha es 0.
        
        # Buscamos todas las ejecuciones completadas por este usuario
        completed_dates = set(
            RoutineExecution.objects.filter(
                user=user, 
                status='COMPLETED'
            ).values_list('actual_end__date', flat=True)
        )
        
        if not completed_dates:
            return 0
            
        if today in completed_dates:
            streak += 1
            current_date = today - timedelta(days=1)
        elif (today - timedelta(days=1)) in completed_dates:
            # Empezamos a contar desde ayer
            current_date = today - timedelta(days=1)
        else:
            return 0

        while current_date in completed_dates:
            streak += 1
            current_date -= timedelta(days=1)
            
        return streak

    @staticmethod
    def get_daily_progress(user) -> list:
        """
        Retorna el progreso diario por categoría.
        """
        # Aseguramos que la agenda esté generada
        get_today_agenda(user)
        
        today = timezone.now().date()
        today_start = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
        today_end = today_start + timedelta(days=1)
        
        executions = RoutineExecution.objects.filter(
            user=user,
            scheduled_start__gte=today_start,
            scheduled_start__lt=today_end
        )
        
        categories = Category.objects.all()
        progress = []
        
        for category in categories:
            cat_executions = executions.filter(routine__category=category)
            total = cat_executions.count()
            if total == 0:
                continue
                
            completed = cat_executions.filter(status='COMPLETED').count()
            progress.append({
                'category_code': category.code,
                'category_name': category.name,
                'color_code': category.color_code,
                'total': total,
                'completed': completed,
                'percentage': int((completed / total) * 100)
            })
            
        return progress

    @staticmethod
    def get_up_next(user) -> dict:
        """
        Retorna la próxima rutina a ejecutar hoy.
        """
        get_today_agenda(user)
        
        today = timezone.now().date()
        today_start = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
        today_end = today_start + timedelta(days=1)
        
        next_execution = RoutineExecution.objects.filter(
            user=user,
            scheduled_start__gte=today_start,
            scheduled_start__lt=today_end,
            status__in=['PENDING', 'SNOOZED']
        ).order_by('scheduled_start').first()
        
        if not next_execution:
            return None
            
        return {
            'id': str(next_execution.id),
            'title': next_execution.routine.title,
            'scheduled_start': next_execution.scheduled_start.isoformat(),
            'category_color': next_execution.routine.category.color_code
        }

    @staticmethod
    def get_dashboard_data(user) -> dict:
        return {
            'current_streak': DashboardService.get_current_streak(user),
            'daily_progress': DashboardService.get_daily_progress(user),
            'up_next': DashboardService.get_up_next(user)
        }
