from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count
from django.db.models.functions import ExtractHour

from apps.executions.models import RoutineExecution
from apps.routines.models import Category

class ReportsService:
    @classmethod
    def get_full_report(cls, user):
        now = timezone.localtime()
        return {
            "weekly_progress": cls.get_weekly_progress(user, now),
            "heatmap": cls.get_heatmap_90_days(user, now),
            "hourly_compliance": cls.get_hourly_compliance(user, now),
            "sleep_vs_focus": cls.get_sleep_vs_focus(user, now)
        }

    @classmethod
    def get_weekly_progress(cls, user, now):
        """
        Retorna arreglo con el porcentaje de cumplimiento de los últimos 7 días.
        Ejemplo: [ { "day": "Mon", "compliance": 80 }, ... ]
        """
        progress = []
        for i in range(6, -1, -1):
            target_date = (now - timedelta(days=i)).date()
            start_of_day = timezone.make_aware(timezone.datetime.combine(target_date, timezone.datetime.min.time()))
            end_of_day = timezone.make_aware(timezone.datetime.combine(target_date, timezone.datetime.max.time()))

            executions_that_day = RoutineExecution.objects.filter(
                user=user,
                scheduled_start__gte=start_of_day,
                scheduled_start__lte=end_of_day
            )
            
            total_count = executions_that_day.count()
            completed_count = executions_that_day.filter(status='COMPLETED').count()
            
            compliance = 0
            if total_count > 0:
                compliance = int((completed_count / total_count) * 100)
            
            progress.append({
                "day": target_date.strftime('%a'),
                "date": target_date.isoformat(),
                "compliance": compliance
            })
            
        return progress

    @classmethod
    def get_heatmap_90_days(cls, user, now):
        """
        Retorna histórico de los últimos 90 días indicando si la racha se mantuvo activa.
        """
        start_date = (now - timedelta(days=89)).date()
        start_datetime = timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
        
        # Obtenemos todas las ejecuciones completadas en los últimos 90 días
        completed_executions = RoutineExecution.objects.filter(
            user=user,
            status='COMPLETED',
            actual_end__gte=start_datetime
        )
        
        # Creamos un set con las fechas donde hubo al menos un completion
        active_dates = set()
        for exec in completed_executions:
            if exec.actual_end:
                active_dates.add(timezone.localtime(exec.actual_end).date())

        heatmap = []
        for i in range(89, -1, -1):
            target_date = (now - timedelta(days=i)).date()
            heatmap.append({
                "date": target_date.isoformat(),
                "active": target_date in active_dates
            })
            
        return heatmap

    @classmethod
    def get_hourly_compliance(cls, user, now):
        """
        Agrupa rutinas completadas en el mes actual por hora del día (actual_end).
        """
        start_of_month = timezone.make_aware(timezone.datetime(now.year, now.month, 1))
        
        executions_this_month = RoutineExecution.objects.filter(
            user=user,
            status='COMPLETED',
            actual_end__gte=start_of_month
        ).annotate(hour=ExtractHour('actual_end')).values('hour').annotate(count=Count('id')).order_by('hour')

        # Formatear la salida para tener 24 horas representadas o solo las que tienen datos
        # Retornaremos todas las horas del día de 0 a 23 para que el front no tenga que rellenar
        hourly_data = {hour: 0 for hour in range(24)}
        for entry in executions_this_month:
            if entry['hour'] is not None:
                # timezone differences can make ExtractHour return UTC hour, but we will assume UTC for now or we can just pass it as is.
                # ExtractHour returns the hour based on the database timezone.
                h = int(entry['hour'])
                if 0 <= h < 24:
                    hourly_data[h] = entry['count']

        result = []
        for hour in range(24):
            # Formato AM/PM
            period = "AM" if hour < 12 else "PM"
            display_hour = hour if hour <= 12 else hour - 12
            if display_hour == 0: display_hour = 12
            
            result.append({
                "hour": f"{display_hour}:00 {period}",
                "hour_24": hour,
                "count": hourly_data[hour]
            })
            
        return result

    @classmethod
    def get_sleep_vs_focus(cls, user, now):
        """
        Extrae horas totales en 'Sleep' vs 'Focus' en los últimos 7 días, agrupado por día.
        """
        results = []
        for i in range(6, -1, -1):
            target_date = (now - timedelta(days=i)).date()
            start_of_day = timezone.make_aware(timezone.datetime.combine(target_date, timezone.datetime.min.time()))
            end_of_day = timezone.make_aware(timezone.datetime.combine(target_date, timezone.datetime.max.time()))

            executions = RoutineExecution.objects.filter(
                user=user,
                status='COMPLETED',
                actual_end__gte=start_of_day,
                actual_end__lte=end_of_day,
                routine__category__code__in=['sleep', 'focus']
            ).values('routine__category__code').annotate(total_minutes=Sum('duration_minutes'))

            day_data = {
                "day": target_date.strftime('%a'),
                "sleep_hours": 0.0,
                "focus_hours": 0.0
            }

            for entry in executions:
                hours = round(entry['total_minutes'] / 60.0, 2) if entry['total_minutes'] else 0.0
                if entry['routine__category__code'] == 'sleep':
                    day_data['sleep_hours'] = hours
                elif entry['routine__category__code'] == 'focus':
                    day_data['focus_hours'] = hours
                    
            results.append(day_data)

        return results
