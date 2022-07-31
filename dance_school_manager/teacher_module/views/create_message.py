from django.shortcuts import render, redirect
from django.views.generic import CreateView

from teacher_module.forms.create_message_form import CreateMessageForm


class MessagePostView(CreateView):

    def get(self, request, *args, **kwargs):
        form = CreateMessageForm(request.POST or None)
        context = {'form': form,
                   }
        return render(request, 'profiles/teacher/create_message.html', context)

    def post(self, request, *args, **kwargs):
        form = CreateMessageForm(request.POST)
        form.instance.user = request.user
        if request.method == "POST":
            if form.is_valid():
                related_course = form.cleaned_data.get("related_course")
                form.save()
                return redirect("teacher_module:course_page_view", course_id=related_course.id)


        context = {'form': form,
           # 'userlist':userlist
           }

        return render(request, 'profiles/teacher/create_message.html', context)
