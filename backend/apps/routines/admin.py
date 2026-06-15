from django.contrib import admin
from .models import Category, RoutineTemplate, RoutineScheduleRule

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'color_code')

class RoutineScheduleRuleInline(admin.TabularInline):
    model = RoutineScheduleRule
    extra = 1

@admin.register(RoutineTemplate)
class RoutineTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'active')
    list_filter = ('active', 'category')
    search_fields = ('title', 'user__username')
    inlines = [RoutineScheduleRuleInline]
