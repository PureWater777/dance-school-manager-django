from django import forms

from authentication_module.models import CustomUser
from courses_module.models import Courses
from teacher_module.models import Message


class CreateMessageForm(forms.ModelForm):
    class Meta:
        model = Message
       # fields = ["title", "text", "user", "related_course"]
        exclude = ["user"]

