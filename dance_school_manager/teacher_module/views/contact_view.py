from django.shortcuts import render


def contact_view(request):
    return render(request, template_name='profiles/teacher/contact.html')
