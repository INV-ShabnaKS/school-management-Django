from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        if options.get('role'):
            options['role'] = options['role'].title()
        super().handle(*args, **options)
