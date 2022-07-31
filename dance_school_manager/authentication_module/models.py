from datetime import timedelta, datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpResponse
from django.utils import timezone

from authentication_module.managers import UserManager
from courses_module.models import Courses
from dance_school_manager.settings import IMAGES_ROOT

EMPLOYEE = 'employee'
TEACHER = 'teacher'
STUDENT = 'student'
UNKNOWN = 'unknown'


class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to=IMAGES_ROOT, blank=True, default=None, null=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    deposit = models.IntegerField(verbose_name="deposit of monet", default=50)

    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    courses = models.ManyToManyField(Courses, blank=True)

    objects = UserManager()

    def get_user_type(self) -> str:
        if self.is_employee:
            return EMPLOYEE
        elif self.is_teacher:
            return TEACHER
        elif self.is_student:
            return STUDENT
        else:
            return UNKNOWN

    def __str__(self):
        return f'{self.email}: {self.username}'

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    def get_aboslut_absences(self):
        return [course.related_course for course in MissedCourse.objects.filter(related_student__id=self.id)]

    def get_absences(self):
        absences = MissedCourse.objects.filter(related_student__id=self.id)
        ongoing = self.get_ongoing_courses(timedelta(minutes=+15))
        result = []
        for course in absences:
            if course.related_course not in ongoing:
                result.append(course)
        return result

    def get_ongoing_courses(self, time_delta: timedelta):
        courses = self.courses.all()
        current_courses = []
        for course in courses:
            if course.is_ongoing(time_delta):
                current_courses.append(course)
        return current_courses

    def get_reported_absences(self):
        reported_absences = ReportedAbsences.objects.filter(related_student__id=self.id)
        return reported_absences


class MissedCourse(models.Model):
    date = models.DateField()
    related_student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, unique=False)
    related_course = models.ForeignKey(Courses, on_delete=models.CASCADE, unique=False)
    is_deposit_substracted = models.BooleanField(default=False)

    def __str__(self):
        return f'MissedCourse: {self.date}, {self.related_course}'

    @property
    def date_to_url(self):
        return datetime.strptime(str(self.date), '%Y-%m-%d')


def set_absence_for_ongoing_courses(request=None):
    for course in Courses.objects.all():
        if course.is_ongoing(timedelta(minutes=+15)):
            for student in CustomUser.objects.filter(courses__id=course.id, is_student=True):
                for absence in student.get_reported_absences():
                    if absence.related_course == course:
                        to_delete = ReportedAbsences.objects.filter(id=absence.id)
                        to_delete.delete()
                        continue
                else:
                    m = MissedCourse(date=timezone.now().date(), related_student=student, related_course=course)
                    m.save()


class ReportedAbsences(models.Model):
    date = models.DateField()
    related_course = models.ForeignKey(Courses, on_delete=models.CASCADE, unique=False)
    related_student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, unique=False)
