from django.shortcuts import render
from django.views.generic import CreateView


class CalendarViews(CreateView):
    template = 'profiles/teacher/calendar_view.html'

    def get(self, request, *args, **kwargs):
        courses_list = request.user.courses.all()
        monday = [course for course in courses_list if course.days == '0']
        tuesday = [course for course in courses_list if course.days == '1']
        wednesday = [course for course in courses_list if course.days == '2']
        thursday = [course for course in courses_list if course.days == '3']
        friday = [course for course in courses_list if course.days == '4']

        context = {'monday': monday,
                   'tuesday': tuesday,
                   'wednesday': wednesday,
                   'thursday': thursday,
                   'friday': friday,
                   'user': request.user, }

        return render(request, self.template, context=context)