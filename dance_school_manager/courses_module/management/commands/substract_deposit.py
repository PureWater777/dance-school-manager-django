from django.core.management import BaseCommand

from employee_module.views.student.edit_student_view import substract_deposit


class Command(BaseCommand):
    help = 'Set absences everyone on course that is now ongoing'

    def handle(self, *args, **kwargs):
        substract_deposit()
