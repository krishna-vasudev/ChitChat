from django.db import models
from datetime import datetime

from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

# Create your models here.

class Message(models.Model):
    sender=models.CharField(max_length=120)
    receiver=models.CharField(max_length=120)
    message=models.CharField(max_length=1000000)
    date=models.DateTimeField(default=datetime.now,blank=True)
    file_status=models.BooleanField(default=False)
    file_name=models.CharField(max_length=1000000,default=None,null=True)

class Friend(models.Model):
    user=models.CharField(max_length=120)
    friend=models.CharField(max_length=120)
    nickname=models.CharField(max_length=120)

class Fileupload(models.Model):
    file=models.FileField(upload_to='uploaded_files/', storage=gd_storage)
