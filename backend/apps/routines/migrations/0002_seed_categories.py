# Generated automatically
from django.db import migrations

def seed_categories(apps, schema_editor):
    Category = apps.get_model('routines', 'Category')
    categories = [
        {'code': 'hygiene', 'name': 'Higiene', 'color_code': 'var(--hygiene-color)'},
        {'code': 'exercise', 'name': 'Ejercicio', 'color_code': 'var(--exercise-color)'},
        {'code': 'focus', 'name': 'Foco', 'color_code': 'var(--focus-color)'},
        {'code': 'nutrition', 'name': 'Alimentación', 'color_code': 'var(--nutrition-color)'},
        {'code': 'sleep', 'name': 'Sueño', 'color_code': 'var(--sleep-color)'},
    ]
    for cat in categories:
        Category.objects.get_or_create(code=cat['code'], defaults=cat)

def reverse_seed(apps, schema_editor):
    Category = apps.get_model('routines', 'Category')
    Category.objects.filter(code__in=['hygiene', 'exercise', 'focus', 'nutrition', 'sleep']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('routines', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_categories, reverse_seed),
    ]
