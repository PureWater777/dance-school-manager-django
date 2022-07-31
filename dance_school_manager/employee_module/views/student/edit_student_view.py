from datetime import timedelta, datetime
from typing import List

from django.shortcuts import get_object_or_404, redirect

from authentication_module.models import CustomUser, MissedCourse
from courses_module.models import Courses
from dance_school_manager.settings import MISSED_COURSE_PENALTY
from employee_module.forms.student.create_student_form import EditStudentForm
from employee_module.views.base.edit_user_view import EditUserView


class EditStudentView(EditUserView):
    template = 'profiles/employee/student/edit_student_view.html'
    user_form = EditStudentForm
    user_role = 'is_student'

    def get(self, request, user_id: int):
        student = get_object_or_404(CustomUser, id=user_id)
        absences_to_show: List[Courses] = student.get_absences()
        ongoing_courses = student.get_ongoing_courses(timedelta(minutes=15))
        marked_as_present = get_marked_as_present(ongoing_courses, student.get_aboslut_absences())
        date = datetime.now().date()
        additional_context = {'ongoing_courses': ongoing_courses,
                              'deposit': student.deposit,
                              'student_id': student.id,
                              'absences': absences_to_show,
                              'marked_as_present': marked_as_present,
                              'date': date,
                              }
        return super(EditStudentView, self).get(request, user_id, additional_context)

    def post(self, request, user_id: int):
        student = get_object_or_404(CustomUser, id=user_id)
        additional_context = {
            'deposit': student.deposit,
        }
        return super(EditStudentView, self).post(request, user_id, additional_context)



def set_present(request, date, user_id, course_id):
    missed_course = MissedCourse.objects.filter(date=date, related_student__id=user_id, related_course__id=course_id)
    missed_course.delete()
    return redirect(f'/employee/edit_student/{user_id}/')


def get_marked_as_present(ongoing, absences):
    result = []
    for course in ongoing:
        if course not in absences:
            result.append(course)
    return result


def substract_deposit(request=None):
    all_students = CustomUser.objects.filter(is_student=True)
    for student in all_students:
        for missed_course in MissedCourse.objects.filter(related_student__id=student.id):
            if not missed_course.is_deposit_substracted:
                if student.deposit > 0:
                    student.deposit -= MISSED_COURSE_PENALTY
                    student.save()


def remove_course_from_student(request, course_name, student_id):
    if course_name != "None":
        user = CustomUser.objects.get(pk=student_id)
        if user.is_student:
            user.courses.remove(Courses.objects.get(name=course_name))
            user.save()
    return redirect(f'/employee/edit_student/{student_id}')


def remove_course_from_teacher(request, course_name, teacher_id):
    if course_name != "None":
        user = CustomUser.objects.get(pk=teacher_id)
        if user.is_teacher:
            user.courses.remove(Courses.objects.get(name=course_name))
            user.save()
    return redirect(f'/employee/edit_teacher/{teacher_id}')
