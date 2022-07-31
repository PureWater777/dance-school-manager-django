from django.contrib.auth.decorators import login_required
from django.urls import path

from employee_module.urls import login_url
from teacher_module.views.calendar import CalendarViews
from teacher_module.views.contact_view import contact_view
from teacher_module.views.course_page import CoursePageViews, CoursesViews
from teacher_module.views.create_message import MessagePostView
from teacher_module.views.main_view import TeacherView
from teacher_module.views.settings_view import SettingsViews
from teacher_module.views.view_courses import CoursesListViews

app_name = "teacher_module"

urlpatterns = [
    path('', login_required(TeacherView.as_view(), login_url=login_url), name='teacher_profile_view'),
    path('courses_list/', login_required(CoursesListViews.as_view(), login_url=login_url), name='courses_list_view'),
    path('settings/', login_required(SettingsViews.as_view(), login_url=login_url), name='settings_view'),
    path('calendar/', login_required(CalendarViews.as_view(), login_url=login_url), name='calendar_view'),
    path('courses/', login_required(CoursesViews.as_view(), login_url=login_url), name='courses_view'),
    path('certain_course/<int:course_id>/', login_required(CoursePageViews.as_view(), login_url=login_url),
         name='course_page_view'),
    path('certain_course/create_message/', login_required(MessagePostView.as_view(), login_url=login_url),
         name='create_message_view'),
    path('contacts/', contact_view, name='contact_view')
]
