from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path("",views.home,name='home'),
    path("room/<str:friendusername>",views.room,name='room'),
    path("checkview",views.checkview,name='checkview'),
    path("send",views.send,name='send'),
    path("getmessages/<str:friend>",views.getmessages,name='getmessages'),
    path("friends",views.friends,name='friends'),
    path("removefriend",views.removefriend,name='removefriend'),
    path("uploadfiles/<str:friend>",views.uploadfiles,name='uploadfiles'),
]