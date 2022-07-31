from authentication_module.models import CustomUser
from employee_module.forms.student.create_student_form import CreateStudentForm
from employee_module.views.base.create_user_view import CreateUserView


class CreateStudentView(CreateUserView):
    template = 'profiles/employee/student/edit_student_view.html'
    user_form = CreateStudentForm
    user_role = 'is_student'

    def assign_data_to_new_user_object(self, user_form):
        name = user_form.cleaned_data['username']
        email = user_form.cleaned_data['email']
        password = user_form.cleaned_data['password']
        student = CustomUser(username=name, email=email, password=password, is_student=True)
        student.save()
        return student
