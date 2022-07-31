from typing import Callable

from django.db.models import QuerySet
from django.shortcuts import render, get_object_or_404

from authentication_module.models import CustomUser
from courses_module.models import Courses
from employee_module.views.base.create_user_view import CreateUserView


class EditUserView(CreateUserView):
    template = ''
    user_form: Callable

    def get(self, request, user_id, additional_context={}):
        user = get_object_or_404(CustomUser, id=user_id)
        courses: QuerySet = user.courses.all()

        user_form = self.user_form(initial={'username': user.username, 'email': user.email})
        for i, course in enumerate(courses):
            user_form.initial.update({f'{i}_course': course.name})

        local_context = {'user_form': user_form,
                         'username': request.user.username,
                         'avatar': request.user.avatar,
                         }
        local_context.update(self.context)
        local_context.update(additional_context)
        return render(request, self.template, local_context)

    def post(self, request, user_id: int, additional_context = {}):
        user_form = self.user_form(request.POST)
        local_context = {'user_form': user_form}
        local_context.update(self.context)
        local_context.update(additional_context)
        user = get_object_or_404(CustomUser, id=user_id)
        if user_form.is_valid():
            courses_not_found = []
            for field in user_form.fields.keys():
                if field.endswith('course'):
                    course_name = user_form.cleaned_data[field]
                    try:
                        if course_name:
                            self.assign_course_to_user(user=user, course_name=course_name)
                    except Courses.DoesNotExist:
                        courses_not_found.append(course_name)
            if courses_not_found:
                local_context.update({'courses_not_found': courses_not_found})
                return render(request, self.template, local_context)
            user.username = user_form.cleaned_data['username']
            user.email = user_form.cleaned_data['email']
            user.save()
            local_context.update({'warrning': f'You edited user {str(user)}'})
            return render(request, self.template, local_context)
        else:
            local_context.update({'warrning': str(user_form.errors)})
            return render(request, self.template, local_context)
