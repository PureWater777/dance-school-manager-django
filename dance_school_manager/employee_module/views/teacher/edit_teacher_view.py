from django.shortcuts import get_object_or_404

from authentication_module.models import CustomUser
from employee_module.forms.teacher.create_teacher_form import EditTeacherForm
from employee_module.views.base.edit_user_view import EditUserView


class EditTeacherView(EditUserView):
    template = 'profiles/employee/teacher/edit_teacher_view.html'
    user_form = EditTeacherForm
    user_role = 'is_teacher'

    def get(self, request, user_id: int):
        student = get_object_or_404(CustomUser, id=user_id)
        additional_context = {'student_id': student.id}
        return super(EditTeacherView, self).get(request, user_id, additional_context)

    def post(self, request, user_id: int):
        student = get_object_or_404(CustomUser, id=user_id)
        additional_context = {'student_id': student.id}
        return super(EditTeacherView, self).post(request, user_id, additional_context)
