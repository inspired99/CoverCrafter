from django.db import models


class VideoFile(models.Model):
    actual_path = models.CharField(max_length=100)
    name = models.CharField(max_length=60)
    eof = models.BooleanField()


class UserPhoto(models.Model):
    face_picture = models.ImageField(upload_to='face/')
