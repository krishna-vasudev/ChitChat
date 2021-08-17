from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path("login",views.loginUser,name='login'),
    path("logout",views.logoutuser,name='logout'),
    path("signup",views.signupuser,name='signup'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('forgotpassword',views.forgotpassword,name='forgotpassword'),
    path('passwordresetvalidation/<uidb64>/<token>/',views.passwordresetvalidation, name='passwordresetvalidation'),
    path('passwordreset',views.passwordreset,name='passwordreset'),

]