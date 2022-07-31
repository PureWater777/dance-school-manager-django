from django.contrib.auth.decorators import login_required
from django.http import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View, generic
from django.views.generic import DeleteView, UpdateView
from django.contrib.auth.forms import UserChangeForm

from django.views.generic import CreateView


class SchoolCoursesViews(CreateView):
    template_name = 'profiles/teacher/school_courses_view.html'