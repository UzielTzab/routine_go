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
        executions = get_today_agenda(user)
        
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
        executions = get_today_agenda(user)
        
        next_execution = executions.filter(
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
    def get_weekly_compliance(user) -> dict:
        """
        Calculates compliance for the last 7 days (including today).
        """
        today = timezone.now().date()
        start_date = today - timedelta(days=6)
        
        days_map = {0: 'M', 1: 'T', 2: 'W', 3: 'T', 4: 'F', 5: 'S', 6: 'S'}
        
        executions = RoutineExecution.objects.filter(
            user=user,
            scheduled_start__date__gte=start_date,
            scheduled_start__date__lte=today
        ).exclude(status__in=['SNOOZED', 'NOTIFIED', 'PENDING']) # Only count resolved items for past days
        
        # We need a structure per day
        days_data = []
        total_percentage = 0
        days_counted = 0
        
        for i in range(7):
            current = start_date + timedelta(days=i)
            day_execs = executions.filter(scheduled_start__date=current)
            total = day_execs.count()
            
            if current == today:
                # For today, we consider ALL scheduled routines for compliance calculation
                # including pending ones.
                total = RoutineExecution.objects.filter(
                    user=user,
                    scheduled_start__date=today
                ).count()
                
            completed = day_execs.filter(status='COMPLETED').count()
            
            progress = int((completed / total * 100)) if total > 0 else 0
            
            # If it's a past day and there were no routines, progress is 0 but maybe we don't count it towards AVG?
            # Let's count it.
            if total > 0 or current == today:
                total_percentage += progress
                days_counted += 1
                
            days_data.append({
                'day': days_map[current.weekday()],
                'progress': progress,
                'is_today': current == today
            })
            
        avg = int(total_percentage / days_counted) if days_counted > 0 else 0
        
        return {
            'average': avg,
            'days': days_data
        }

    @staticmethod
    def get_active_routine(user) -> dict:
        """
        Returns the currently IN_PROGRESS routine if any.
        """
        active = RoutineExecution.objects.filter(
            user=user,
            status='IN_PROGRESS'
        ).first()
        
        if not active:
            return None
            
        duration = active.duration_minutes if active.duration_minutes else active.routine.default_duration_minutes
            
        return {
            'id': str(active.id),
            'title': active.routine.title,
            'category_name': active.routine.category.name,
            'duration_minutes': duration
        }

    @staticmethod
    def get_dashboard_data(user) -> dict:
        return {
            'current_streak': DashboardService.get_current_streak(user),
            'daily_progress': DashboardService.get_daily_progress(user),
            'up_next': DashboardService.get_up_next(user),
            'weekly_compliance': DashboardService.get_weekly_compliance(user),
            'active_routine': DashboardService.get_active_routine(user)
        }
