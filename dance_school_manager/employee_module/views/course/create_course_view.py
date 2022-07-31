from django.shortcuts import render

from authentication_module.models import CustomUser
from courses_module.models import Courses
from employee_module.forms.course.create_course_form import CreateCourseForm
from employee_module.views.base.manage_user_view import ManageUserView


class CreateCourseView(ManageUserView):
    template = 'profiles/employee/course/create_course_view.html'

    def get(self, request):
        course_form = CreateCourseForm()
        local_context = {'course_form': course_form}
        local_context.update(self.context)
        return render(request, self.template, local_context)

    def post(self, request, *args, **kwargs):
        course_form = CreateCourseForm(request.POST)
        local_context = {'course_form': course_form,
                         'username': request.user.username,
                         'avatar': request.user.avatar, }
        local_context.update(self.context)
        if course_form.is_valid():
            name = course_form.cleaned_data['name']
            description = course_form.cleaned_data['description']
            start_date = course_form.cleaned_data['start_date']
            days = course_form.cleaned_data['days']
            time = course_form.cleaned_data['time']
            end_date = course_form.cleaned_data['end_date']
            course = Courses(name=name, description=description,
                             start_date=start_date, days=days,
                             time=time, end_date=end_date)
            emails_not_found = []

            for student in course_form.fields.keys():
                email = course_form.cleaned_data[student]
                if student.endswith('student') and email:
                    try:
                        self.assign_course_to_student_by(email=email, course=course)
                    except CustomUser.DoesNotExist:
                        emails_not_found.append(email)

            if emails_not_found:
                local_context.update({'emails_not_found': emails_not_found, })
                return render(request, self.template, local_context)
            course.save()
            local_context.update({'warrning': f'You created course {str(course)}'})
            return render(request, self.template, local_context)
        else:
            local_context.update({'warrning': 'Course can not be created'})
            return render(request, self.template, local_context)

    @classmethod
    def assign_course_to_student_by(cls, email, course):
        user = CustomUser.objects.get(email=email)
        if user.is_student:
            user.courses.add(course)
        else:
            raise CustomUser.DoesNotExist
        user.save()
