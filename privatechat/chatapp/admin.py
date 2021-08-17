from django.contrib import admin
from .models import Message,Friend,Fileupload
# Register your models here.
admin.site.register(Message)
admin.site.register(Friend)
admin.site.register(Fileupload)

