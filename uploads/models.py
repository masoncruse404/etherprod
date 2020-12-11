from django.db import models
from django.contrib.auth.models import User
#from profiles.models import Profile
from django.utils import timezone
from django.conf import settings
from django.apps import apps

BASE_DIR = settings.BASE_DIR

from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import CustomUser
#from uploads.models import File, Folder

import os

MAX_STORAGE = 15000000
BASE_DIR = settings.BASE_DIR

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gid = models.IntegerField(default=0)
    storage = models.BigIntegerField(default=0, blank=True)
    capacity = models.BigIntegerField(default=15)
    number = models.IntegerField(default=0)
    timesincelastlogin = models.CharField(max_length=100, blank=True,null=True)
    creationdate = models.DateTimeField(default=timezone.now())
    lastlogin = models.DateTimeField(blank=True,null=True)
    sharedfiles = models.ManyToManyField(to='uploads.File', related_name='sharedfiles')
    sharedfolders = models.ManyToManyField(to='uploads.Folder', related_name='sharedfolders')

    def __str__(self):
        return self.user.email








# Create your models here.
class File(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='file_owner')
    users = models.ManyToManyField(Profile, related_name='file_users')
    path = models.CharField(max_length=500, blank=True)
    name = models.CharField(max_length=500, blank=True)
    file_type = models.CharField(max_length=75, blank=True)
    size = models.BigIntegerField(default=0,blank=True)
    images = models.FileField(blank=True, upload_to='album')
    starred = models.BooleanField(default=False)
    sharedwith = models.ManyToManyField(Profile, related_name='shared_with')
    trash = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(default=timezone.now())
    modified = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name



class Folder(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='folder_owner')
    folderfiles = models.ManyToManyField(File, related_name='folderfiles')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='folder_parent', blank=True, null=True)
    users = models.ManyToManyField(Profile, related_name='folder_users')
    name = models.CharField(max_length=500, blank=True)
    children = models.ManyToManyField('self', related_name='folders')
    path = models.CharField(max_length=500, blank=True)
    starred = models.BooleanField(default=False)
    sharedwith = models.ManyToManyField(Profile, related_name='shared_with_folder')
    #Genesis ID ROOT FOLDER ID
    trash = models.BooleanField(default=False)
    gid = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        pro = Profile.objects.create(user=instance)
        path = BASE_DIR+'/media/accounts/'

        if not os.path.exists(path):
           os.makedirs(path)

        os.chdir(path)
        os.mkdir(path + instance.email)
        os.chdir(path + instance.email)
        os.mkdir('genesis')
        path = path + instance.email + '/genesis/'
        g = Folder.objects.create(path = path, owner=pro, name='genesis')
        pro.gid = g.id
        pro.save()

