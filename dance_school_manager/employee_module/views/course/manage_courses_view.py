from django.shortcuts import render

from courses_module.models import Courses
from employee_module.views.base.manage_user_view import ManageUserView


class ManageCoursesView(ManageUserView):
    template = 'profiles/employee/course/manage_courses_view.html'
    filter_arg = {}
    model = 'courses'

    def get(self, request, *args, **kwargs):
        local_context = {'courses': Courses.objects.all(),
                         'username': request.user.name,
                         'avatar': request.user.avatar,
                         }
        local_context.update(self.context)
        return render(request, self.template, local_context)

    def get_search_result(self, searched):
        return Courses.objects.filter(name__contains=searched)
