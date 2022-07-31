from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView

from authentication_module.forms import StudentSignUpForm
from authentication_module.models import CustomUser
from authentication_module.models import EMPLOYEE, TEACHER, STUDENT


class StudentSignUpView(CreateView):
    model = CustomUser
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponse("Form is valid")


@login_required(login_url='/login/')
def redirect_by_user_type(request):
    logged_user_type: CustomUser = request.user.get_user_type()
    user_type_views = {
        EMPLOYEE: 'employee',
        TEACHER: 'teacher',
        STUDENT: 'client',
    }
    return redirect(f'/{user_type_views[logged_user_type]}/')


def redirect_to_login(request):
    return redirect('authentication/login')
