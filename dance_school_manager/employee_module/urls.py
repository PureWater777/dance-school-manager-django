from django.contrib.auth.decorators import login_required
from django.urls import path, register_converter

from authentication_module.models import set_absence_for_ongoing_courses
from employee_module import url_converter
from employee_module.views.course.create_course_view import CreateCourseView
from employee_module.views.course.edit_course_view import EditCourseView, remove_student_from_course
from employee_module.views.course.manage_courses_view import ManageCoursesView
from employee_module.views.default_employee_view import EmployeeHomeView
from employee_module.views.student.create_student_view import CreateStudentView
from employee_module.views.student.edit_student_view import EditStudentView, set_present, remove_course_from_student, \
    substract_deposit, remove_course_from_teacher
from employee_module.views.student.manage_student_view import ManageStudentsView
from employee_module.views.teacher.create_teacher_view import CreateTeacherView
from employee_module.views.teacher.edit_teacher_view import EditTeacherView
from employee_module.views.teacher.manage_teachers_view import ManageTeachersView

register_converter(url_converter.DateTimeConverter, 'date')
login_url = '/authentication/login'
app_name = 'employee_module'
urlpatterns = [
    path('', login_required(ManageCoursesView.as_view(), login_url=login_url), name='employee_home_view'),

    # courses
    path('create_course/', login_required(CreateCourseView.as_view(), login_url=login_url), name='create_course_view'),
    path('manage_courses/', login_required(ManageCoursesView.as_view(), login_url=login_url),
         name='manage_courses_view'),
    path('edit_course/<int:course_id>/', login_required(EditCourseView.as_view(), login_url=login_url),
         name='edit_course_view'),

    # teachers
    path('manage_teachers/', login_required(ManageTeachersView.as_view(), login_url=login_url),
         name='manage_teachers_view'),
    path('create_teachers/', login_required(CreateTeacherView.as_view(), login_url=login_url),
         name='create_teacher_view'),
    path('edit_teacher/<int:user_id>/', login_required(EditTeacherView.as_view(), login_url=login_url),
         name='edit_teacher_view'),

    # students
    path('manage_students/', login_required(ManageStudentsView.as_view(), login_url=login_url),
         name='manage_students_view'),
    path('create_student/', login_required(CreateStudentView.as_view(), login_url=login_url),
         name='create_student_view'),
    path('edit_student/<int:user_id>/', login_required(EditStudentView.as_view(), login_url=login_url),
         name='edit_student_view'),

    # mechanisms
    # path('set_absances/', set_absence_for_ongoing_courses, name='set_absance'),
    # path('substract_deposit/', substract_deposit, name='substract_deposit'),

    path('set_present/<date:date>/<int:user_id>/<int:course_id>/', set_present, name='set_present'),

    path('remove_from_course/<str:student_email>/<int:course_id>/', remove_student_from_course,
         name='remove_student_from_course'),

    path('remove_course_from_student/<str:course_name>/<int:student_id>/', remove_course_from_student,
         name='remove_course_from_student'),

    path('remove_course_from_teacher/<str:course_name>/<int:teacher_id>/', remove_course_from_teacher,
         name='remove_course_from_teacher'),


]
