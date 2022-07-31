from authentication_module.models import CustomUser
from employee_module.forms.teacher.create_teacher_form import CreateTeacherForm
from employee_module.views.base.create_user_view import CreateUserView


class CreateTeacherView(CreateUserView):
    template = 'profiles/employee/teacher/edit_teacher_view.html'
    user_form = CreateTeacherForm
    user_role = 'is_teacher'

    def assign_data_to_new_user_object(self, user_form):
        name = user_form.cleaned_data['username']
        email = user_form.cleaned_data['email']
        password = user_form.cleaned_data['password']
        student = CustomUser(username=name, email=email, password=password, is_teacher=True)
        student.save()
        return student
