from django.db import migrations

def truncate_teachers(apps, schema_editor):
    Teacher = apps.get_model('teachers', 'Teacher')
    Teacher.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0002_initial'),  
    ]

    operations = [
        migrations.RunPython(truncate_teachers),
    ]
