from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import request, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View, generic
from django.views.generic import CreateView

from authentication_module.models import CustomUser
from courses_module.models import Courses
from teacher_module.models import Message


class CoursesViews(CreateView):
    template_name = 'profiles/teacher/courses.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {'username': request.user.username,
                   'courses_list': request.user.courses.all()
                   }
        return render(request, self.template_name, context=context)


class CoursePageViews(CreateView):
    template_name = 'profiles/teacher/course_page.html'

    @method_decorator(login_required)
    def get(self, request, course_id: int):
        course = get_object_or_404(Courses, id=course_id)
        students_attended_to_this_course: QuerySet = CustomUser.objects.filter(courses__id=course_id)

        certain_course = Courses.objects.get(id=course_id)

        # filter messages assignet to certain course
        messages_assigned_to_this_course: QuerySet = Message.objects.filter(related_course=course_id)



        context = {'username': request.user.username,
                   'courses_list': request.user.courses.all(),
                   'course_id': course_id,
                   'certain_course': certain_course,
                   'students_attended': students_attended_to_this_course,
                   'messages_assigned_to_this_course': messages_assigned_to_this_course

                   }

        return render(request, self.template_name, context=context)
