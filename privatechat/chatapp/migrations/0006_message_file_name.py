# Generated by Django 3.2.3 on 2021-08-10 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0005_alter_fileupload_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file_name',
            field=models.CharField(default=None, max_length=1000000),
        ),
    ]
