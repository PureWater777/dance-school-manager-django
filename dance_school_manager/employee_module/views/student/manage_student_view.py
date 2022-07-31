from authentication_module.models import CustomUser
from employee_module.views.base.manage_user_view import ManageUserView


class ManageStudentsView(ManageUserView):
    template = 'profiles/employee/student/manage_student_view.html'
    filter_arg = {'is_student': True}
    model = 'users'

    def get_search_result(self, searched):
        return CustomUser.objects.filter(username__contains=searched, **self.filter_arg)