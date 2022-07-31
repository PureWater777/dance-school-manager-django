from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from courses_module.models import Courses


class EmployeeView(CreateView):
    template = 'profiles/employee/employee_profile_view.html'
    context = {'manage_courses': 'manage_courses',
               'manage_students': 'manage_students',
               'manage_teachers': 'manage_teachers'
               }

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.context.update({'username': request.user.username,
                             'avatar': request.user.avatar,
                             })

        self.context.update({'courses': Courses.objects.all()})

        return render(request, self.template, context=self.context)
