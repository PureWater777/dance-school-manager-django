from django.shortcuts import render
from django.views import View

from authentication_module.models import CustomUser


class ManageUserView(View):
    template = 'profiles/employee/employee_home_view.html'
    context = {'home_view': '/employee/',
               'manage_courses': '/employee/manage_courses',
               'manage_students': '/employee/manage_students',
               'manage_teachers': '/employee/manage_teachers'
               }
    filter_arg = {}
    model = ''

    def get_search_result(self, searched: str):
        raise NotImplementedError

    def post(self, request):
        searched = request.POST['searched']
        result = self.get_search_result(searched)
        local_context = self.get_default_context(request)
        local_context.update({self.model: result})
        return render(request, self.template, local_context)

    def get(self, request):
        local_context = self.get_default_context(request)
        local_context.update({'users': CustomUser.objects.filter(**self.filter_arg)})
        return render(request, self.template, context=local_context)

    def get_default_context(self, request):
        local_context = {'username': request.user.username,
                         'avatar': request.user.avatar,
                         }
        local_context.update(self.context)
        return local_context
