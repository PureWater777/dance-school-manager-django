from datetime import timedelta, date, datetime
from time import time

from django.db import models

from dance_school_manager.settings import HOUR_FORMAT, DAYS_OF_WEEK


class Courses(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    room = models.IntegerField(default=0)
    start_date = models.DateField()
    days = models.CharField(choices=DAYS_OF_WEEK, default='Monday', max_length=70)
    time = models.TimeField()
    end_date = models.DateField()

    def __str__(self):
        return f'Course {self.name}: {self.description}'

    @property
    def lesson_end(self) -> time:
        end_date = datetime.combine(date.today(), self.time) + timedelta(minutes=45)
        return end_date.time()

    def is_ongoing(self, time_delta: timedelta = timedelta(minutes=0)):
        current_time: time = datetime.now() + time_delta
        if self.start_date <= current_time.date() < self.end_date:
            if int(self.days) == current_time.weekday():
                if self.time.strftime(HOUR_FORMAT) <= current_time.time().strftime(
                        HOUR_FORMAT) < self.lesson_end.strftime(HOUR_FORMAT):
                    return True
        return False


class Exceptions(models.Model):
    name = models.CharField(max_length=20)
    date = models.DateField()
    description = models.CharField(max_length=100)
    related_course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return f'Exception: {self.name} : {self.description}'


class GeneralException(models.Model):
    name = models.CharField(max_length=20)
    date = models.DateField()
    description = models.CharField(max_length=100)

    def __str__(self):
        return f'GeneralException: {self.name} : {self.description}'
