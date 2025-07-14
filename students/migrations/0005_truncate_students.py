from django.db import migrations

def truncate_students(apps, schema_editor):
    Student = apps.get_model('students', 'Student')
    Student.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_remove_student_email_remove_student_phone_number'),  
    ]

    operations = [
        migrations.RunPython(truncate_students),
    ]
