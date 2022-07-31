from django.urls import path, include

from authentication_module.views import StudentSignUpView, redirect_by_user_type


urlpatterns = [
    path('', include('django.contrib.auth.urls'), name='auth_module'),
    path('sign_up/student/', StudentSignUpView.as_view(), name='student_signup'),
    path('login/redirect_by_user_type/', redirect_by_user_type, name='redirect_view'),
]