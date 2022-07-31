from django.core.management import BaseCommand

from authentication_module.models import set_absence_for_ongoing_courses


class Command(BaseCommand):
    help = 'Set absences everyone on course that is now ongoing'

    def handle(self, *args, **kwargs):
        set_absence_for_ongoing_courses()
