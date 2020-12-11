from django.contrib import admin
from .models import Folder,Profile,File

# Register your models here.
admin.site.register(File)
admin.site.register(Folder)
admin.site.register(Profile)


    