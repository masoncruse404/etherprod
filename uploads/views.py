


import time
import os
import pytz
import re
import shutil
import json


from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import File, Folder, Photo, Profile
from django.core.files import File as DjangoFile
from datetime import date, datetime, timedelta
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import CustomUser
from django.conf import settings
from analytics.signals import object_viewed_signal



lastParent = None


BASE_DIR = settings.BASE_DIR
User = get_user_model()

GENESIS = BASE_DIR + 'media/accounts'

def getgenesis(pro):
    genesis = BASE_DIR + '/media/accounts/' + str(pro.user.email) + '/genesis/'
    return genesis
def range(min=5):
    return range(min)

def getstoragevalue(pro):
    storage = 100*getstoragegb(pro)
    storage = storage / pro.capacity


    return storage

def checkstorage(pro, uploadsize):
    capacity = pro.capacity * 1000000000
    storage = pro.storage
    if storage + uploadsize > capacity:
        return False
    else:
        return True



def getstoragemb(pro):
    storagemb = pro.storage
    storagemb = int(storagemb/1000000)
    return storagemb

def getstoragegb(pro):
    storagemb = getstoragemb(pro)
    storagegb = storagemb/1024


    return storagegb

def getstorage(pro):
    storage = 100*getstoragegb(pro)
    storage = storage / pro.capacity

    #format storage for progress bar
    storage = str(storage) + '%'

    return storage





#returns context for templates
def getcontext(request):
    user = request.user
    email = user.email
    pro = Profile.objects.get(user=user)
    storagevalue = pro.storage
    

    number = pro.number
    uid = user.id
    cuser = User.objects.get(email=email)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)

    me = user.email
    
    image_list = File.objects.filter(owner=pro,trash=False)
    folder_list = None
    con = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g, trash=False)
    qa_list = []
    x = 0
    all_folder_list = Folder.objects.filter(owner=pro)

    if(image_list):
        for image in image_list:
            if 'jpeg' or 'png' or 'jpg' in image.file_type:
                x = x + 1
                if x == 20:
                    return con
                qa_list.append(image)
                con = {"email":email,"firstinitial":firstinitial,"name":name,"me":me,"storagemb":storagemb,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list, 'storage':storage, 'all_folder_list':all_folder_list,"number":number,"storagevalue":storagevalue}

    con = {"email":email,"firstinitial":firstinitial,"name":name,"me":me,"storagemb":storagemb,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list, 'storage':storage, 'all_folder_list':all_folder_list,"number":number,"storagevalue":storagevalue}

    return con

#get context for trash views

def getcontexttrash(request):
    user = request.user
    pro = Profile.objects.get(user=user)
    storagevalue = pro.storage
    email = user.email
    uid = user.id
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    me = user.email
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)

    me = user.email
   
    image_list = File.objects.filter(owner=pro,trash=True)
    folder_list = None
    con = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g, trash=True)
    all_folder_list = Folder.objects.filter(owner=pro)

    con = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"me":me,"storagemb":storagemb,"image_list":image_list,  'folder_list':folder_list, 'storage':storage, 'all_folder_list':all_folder_list}
    return con


def getcontextstar(request):
    user = request.user
    pro = Profile.objects.get(user=user)
    storagevalue = pro.storage
    email = user.email
    uid = user.id
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()

    me = user.email
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)

    me = user.email
    
    image_list = File.objects.filter(owner=pro,starred=True)
    folder_list = None
    con = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g, starred=True)
 
    all_folder_list = Folder.objects.filter(owner=pro)

    con = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"me":me,"storagemb":storagemb,"image_list":image_list,  'folder_list':folder_list, 'storage':storage, 'all_folder_list':all_folder_list}
    return con



@login_required(login_url='/users/login/')
def recent(request):
    user = request.user
    pro = Profile.objects.get(user=user)
    storagevalue = pro.storage
    email = user.email
    uid = user.id
    cuser = User.objects.get(id=uid)  
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    image_list = File.objects.filter(owner=pro)
    today_list = []
    week_list = []
    month_list = []
    year_list = []
    sep = ' '
    today = datetime.now()
    week = datetime.now() - timedelta(days=7)
    month = datetime.now() - timedelta(days=28)
    year = datetime.now() - timedelta(days=365)
    today = pytz.utc.localize(today)
    todaysplit = str(today).split()
    week = pytz.utc.localize(week)
    month = pytz.utc.localize(month)
    year = pytz.utc.localize(year)
    for image in image_list:
        rest = image.modified
        restsplit = str(rest).split()
        #rest = pytz.utc.localize(rest)
        if rest < year:
            year_list.append(image)
        elif rest <= month:
            month_list.append(image)
        elif rest <= week:
            week_list.append(image)
        elif str(restsplit[0]) ==  str(todaysplit[0]):
            today_list.append(image)


    context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"today_list":today_list, 'week_list':week_list, 'month_list':month_list, 'year_list':year_list, "storage":storage,"storagemb":storagemb}


    return render(request, 'uploads/recent.html', context)
@csrf_exempt
@login_required(login_url='/users/login/')
def mydrive(request):

    context = getcontext(request)
    return render(request, 'uploads/my-drive.html', context)

@csrf_exempt
@login_required(login_url='/users/login/')
def mydrivetest(request):
    context = getcontext(request)
    return render(request, 'uploads/my-drive-test.html', context)

@csrf_exempt
@login_required(login_url='/users/login/')
def mydrivetable(request):
    context = getcontext(request)
    return render(request, 'uploads/my-drive-table-old.html', context)

@csrf_exempt
@login_required(login_url='/users/login/')
def mydrivetableimagesearch(request):
    context = getcontext(request)
    return render(request, 'uploads/my-drive-table.html', context)


@csrf_exempt
@login_required(login_url='/users/login/')
def mydrivetrash(request):

    context = getcontexttrash(request)

    return render(request, 'uploads/my-drive-trash.html', context)


@login_required(login_url='/users/login/')
def removetrash(request, slug, pk):
    #remove file from trash
    f = File.objects.get(pk=pk)
    f.trash = False
    f.save()

    #get trash context
    context = getcontexttrash(request)



    #add message and alert to context
    successmsg = f.name + ' removed from trash '
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})

    return render(request, 'uploads/my-drive-trash.html', context)

@login_required(login_url='/users/login/')
def removetrashtable(request, slug, pk):
    #remove file from trash
    f = File.objects.get(pk=pk)
    f.trash = False
    f.save()

    #get trash context
    context = getcontexttrash(request)



    #add message and alert to context
    successmsg = f.name + ' removed from trash '
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})

    return render(request, 'uploads/my-drive-table-trash.html', context)

@login_required(login_url='/users/login/')
def removetrashfolder(request, slug, pk):
    #remove folder from trash
    f = Folder.objects.get(pk=pk)
    for fi in f.folderfiles.all():
        fi.trash = False
        fi.save()
    f.trash = False
    f.save()


    #get default non trash context
    context = getcontext(request)


    #add message and alert to context
    successmsg = f.name + ' removed from trash '
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})

    return render(request, 'uploads/my-drive.html', context)


@login_required(login_url='/users/login/')
def removetrashfoldertable(request, slug, pk):
    #remove folder from trash
    f = Folder.objects.get(pk=pk)
    for fi in f.folderfiles.all():
        fi.trash = False
        fi.save()
    f.trash = False
    f.save()


    #get default non trash context
    context = getcontext(request)


    #add message and alert to context
    successmsg = f.name + ' removed from trash '
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})

    return render(request, 'uploads/my-drive-table-old.html', context)


@login_required(login_url='/users/login/')
def trash(request, slug, pk):
    context = getcontexttrash(request)
    pro = Profile.objects.get(user=request.user)

    f = File.objects.get(pk=pk)
    if f.trash:
        if f.path:
            if os.path.isdir(f.path):  
                os.remove(f.path+'/'+f.name)
            elif os.path.isfile(BASE_DIR+f.path):  
                os.remove(BASE_DIR+f.path)
        pro.storage -= float(f.size)
        pro.save()
        f.delete()
        successmsg = f.name + ' has been deleted'
    else:
        successmsg = f.name + ' has been added to the trash'
        f.trash = True
        f.save()

    context.update({'successmsg':successmsg})
    context.update({'successalert':1})

    return render(request, 'uploads/my-drive-trash.html', context)


@login_required(login_url='/users/login/')
def trashtable(request, slug, pk):
    context = getcontexttrash(request)
    pro = Profile.objects.get(user=request.user)
    f = File.objects.get(pk=pk)
    if f.trash:
        if f.path:
            os.remove(BASE_DIR+f.path)
           
           
        pro.storage -= float(f.size)
        pro.save()
        f.delete()
        successmsg = f.name + ' has been deleted'
    else:
        successmsg = f.name + ' has been added to the trash'
        f.trash = True
        f.save()

    context.update({'successmsg':successmsg})
    context.update({'successalert':1})

    return render(request, 'uploads/my-drive-table-trash.html', context)

@login_required(login_url='/users/login/')
def trashfolder(request, slug, pk):
    context = getcontexttrash(request)
    pro = Profile.objects.get(user=request.user)
    f = Folder.objects.get(pk=pk)
    if f.trash:
        dirwalkdelete(pro,f)
        successmsg = f.name + ' has been deleted'
        shutil.rmtree(f.path)
        f.delete()
    else:
        successmsg = f.name + ' has been added to the trash'
        f.trash = True
        dirwalktrash(pro,f)
        f.save()

    context.update({'successmsg':successmsg})
    context.update({'successalert':1})
    
    return render(request, 'uploads/my-drive-trash.html', context)


@login_required(login_url='/users/login/')
def trashtablefolder(request, slug, pk):
    context = getcontexttrash(request)
    pro = Profile.objects.get(user=request.user)
    f = Folder.objects.get(pk=pk)
    if f.trash:
        if os.path.exists(f.path):
            shutil.rmtree(f.path)
        for fi in f.folderfiles.all():
            pro.storage -= fi.size
            pro.save()
            fi.delete()
        f.delete()

        successmsg = f.name + ' has been deleted'
    else:
        successmsg = f.name + ' has been added to the trash'
        f.trash = True
        dirwalktrash(pro,f)
        f.save()
    folder_list = Folder.objects.filter(owner=pro, trash=True)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list, 'folder_list':folder_list, 'storage':storage,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/my-drive-table-trash.html', context)



@login_required(login_url='/users/login/')
def allStarred(request):
    context = getcontextstar(request)
    return render(request, 'uploads/my-drive-star.html', context)

@login_required(login_url='/users/login/')
def mydrivestartable(request):
    context = getcontextstar(request)
    return render(request, 'uploads/my-drive-table-star.html', context)

@login_required(login_url='/users/login/')
def mydrivetrashtable(request):
    context = getcontexttrash(request)
    return render(request, 'uploads/my-drive-table-trash.html', context)

@login_required(login_url='/users/login/')
def star(request, slug, pk):
    context = getcontextstar(request)

    f = File.objects.get(pk=pk)
    f.starred = True
    f.save()

    successmsg = f.name + ' is starred'
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})
    return render(request, 'uploads/my-drive-star.html', context)


@login_required(login_url='/users/login/')
def startable(request, slug, pk):
    pro = Profile.objects.get(user=request.user)
    #star file
    f = File.objects.get(pk=pk)
    f.starred = True
    f.save()
    successmsg = f.name + ' is starred'

    #get context
    context = getcontextstar(pro)
    successmsg = f.name + ' is starred'
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})
    return render(request, 'uploads/my-drive-table-star.html', context)

@login_required(login_url='/users/login/')
def starfolder(request, slug, pk):

    f = Folder.objects.get(pk=pk)
    f.starred = True
    f.save()

    context = getcontextstar(request)
    successmsg = f.name + ' is starred'
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})

    return render(request, 'uploads/my-drive-star.html', context)

@login_required(login_url='/users/login/')
def startablefolder(request, slug, pk):
   
    f = Folder.objects.get(pk=pk) 
    f.starred = True
    f.save()
    
    context = getcontextstar(request)
    successmsg = f.name + ' is starred'
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})

    
    return render(request, 'uploads/my-drive-table-star.html', context)

@login_required(login_url='/users/login/')
def removestar(request, slug, pk):
    f = File.objects.get(pk=pk)
    f.starred = False
    f.save()

    warningmsg = f.name + ' has been removed from starred'
    context = getcontextstar(request)
    context.update({'warningmsg':warningmsg})
    context.update({'alert':1})

  
    return render(request, 'uploads/my-drive-star.html', context)

@login_required(login_url='/users/login/')
def removestartable(request, slug, pk):
   
    f = File.objects.get(pk=pk)
    f.starred = False
    f.save()

    warningmsg = f.name + ' has been removed from starred'
    context = getcontextstar(request)
    context.update({'warningmsg':warningmsg})
    context.update({'alert':1})
    return render(request, 'uploads/my-drive-table-star.html', context)

@login_required(login_url='/users/login/')
def removefolderstar(request, slug, pk):
    
    f = Folder.objects.get(pk=pk)
    f.starred = False
    f.save()

    warningmsg = f.name + ' has been removed from starred'
    context = getcontextstar(request)
    context.update({'warningmsg':warningmsg})
    context.update({'alert':1})
    return render(request, 'uploads/my-drive-star.html', context)


#rename file
@csrf_exempt
@login_required(login_url='/users/login/')
def rename(request, slug, pk):
  
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    newname = request.POST.get('popup-input-q','')
    if newname == '':
        warningmsg = 'enter a name'
        context = getcontext(request)
        context.update({"warningmsg":warningmsg})
        context.update({"alert":1})
        return render(request, 'uploads/my-drive.html', context)
    newname = newname+'.'+f.file_type
    if f.starred:
        isStarred = True
    else:
        isStarred = False
    oldname = f.name
    f.name = newname
    successmsg = 'renamed file ' + oldname + ' to file ' + f.name
    f.save()

    context = getcontext(request)
    context.update({"successmsg":successmsg})
    context.update({"successalert":1})

    return render(request, 'uploads/my-drive.html', context)

#rename file
@csrf_exempt
@login_required(login_url='/users/login/')
def renametable(request, slug, pk):
    
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    newname = request.POST.get('popup-input-q','')
    if newname == '':
        warningmsg = 'enter a name'
        context = getcontext(request)
        context.update({"warningmsg":warningmsg})
        context.update({"alert":1})
        return render(request, 'uploads/my-drive-table-old.html', context)
    newname = newname+'.'+f.file_type
    if f.starred:
        isStarred = True
    else:
        isStarred = False
    oldname = f.name
    f.name = newname
    successmsg = 'renamed file ' + oldname + ' to file ' + f.name
    f.save()

    context = getcontext(request)
    context.update({"successmsg":successmsg})
    context.update({"successalert":1})
    

    return render(request, 'uploads/my-drive-table-old.html', context)


#rename file
@csrf_exempt
@login_required(login_url='/users/login/')
def renametrashtable(request, slug, pk):
    
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    newname = request.POST.get('popup-input-q','')
    if newname == '':
        warningmsg = 'enter a name'
        context = getcontexttrash(request)
        context.update({"warningmsg":warningmsg})
        context.update({"alert":1})
        return render(request, 'uploads/my-drive-table-trash.html', context)
    newname = newname+'.'+f.file_type
    if f.starred:
        isStarred = True
    else:
        isStarred = False
    oldname = f.name
    f.name = newname
    successmsg = 'renamed file ' + oldname + ' to file ' + f.name
    f.save()

    context = getcontexttrash(request)
    context.update({"successmsg":successmsg})
    context.update({"successalert":1})
    return render(request, 'uploads/my-drive-table-trash.html', context)


#rename file
@csrf_exempt
@login_required(login_url='/users/login/')
def renamestartable(request, slug, pk):
    
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    newname = request.POST.get('popup-input-q','')
    if newname == '':
        warningmsg = 'enter a name'
        context = getcontextstar(request)
        context.update({"warningmsg":warningmsg})
        context.update({"alert":1})
        return render(request, 'uploads/my-drive-table-star.html', context)
    newname = newname+'.'+f.file_type
    if f.starred:
        isStarred = True
    else:
        isStarred = False
    oldname = f.name
    f.name = newname
    successmsg = 'renamed file ' + oldname + ' to file ' + f.name
    f.save()
    context = getcontextstar(request)
    context.update({"successmsg":successmsg})
    context.update({"successalert":1})

    context = getcontextstar(request)

    return render(request, 'uploads/my-drive-table-star.html', context)




#rename file
@csrf_exempt
@login_required(login_url='/users/login/')
def renamestar(request, slug, pk):
    
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    newname = request.POST.get('popup-input-q','')
    if newname == '':
        warningmsg = 'enter a name'
        context = getcontextstar(request)
        context.update({"warningmsg":warningmsg})
        context.update({"alert":1})
        return render(request, 'uploads/my-drive.html', context)
    newname = newname+'.'+f.file_type
    if f.starred:
        isStarred = True
    else:
        isStarred = False
    oldname = f.name
    f.name = newname
    successmsg = 'renamed file ' + oldname + ' to file ' + f.name
    f.save()

    context = getcontextstar(request)
    context.update({"successmsg":successmsg})
    context.update({"successalert":1})

    return render(request, 'uploads/my-drive-star.html', context)

#rename file
@csrf_exempt
@login_required(login_url='/users/login/')
def renametrash(request, slug, pk):
  
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    newname = request.POST.get('popup-input-q','')
    if newname == '':
        warningmsg = 'enter a name'
        context = getcontexttrash(request)
        context.update({"warningmsg":warningmsg})
        context.update({"alert":1})
        return render(request, 'uploads/my-drive', context)
    oldname = f.name
    newname = newname+'.'+f.file_type

    f.name = newname
    successmsg = 'renamed file ' + oldname + ' to file ' + f.name
    f.save()

    context = getcontexttrash(request)
    context.update({"successmsg":successmsg})
    context.update({"successalert":1})


    return render(request, 'uploads/my-drive-trash.html', context)


#rename a file in a subfolder
@csrf_exempt
@login_required(login_url='/users/login/')
def renamesub(request, slug, pk):
    user = request.user
    pro = Profile.objects.get(user=user)
    storagevalue = pro.storage
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    pf = Folder.objects.get(id=request.session['fid'])
    folder_list = Folder.objects.filter(parent=pf)
    
    all_folder_list = Folder.objects.filter(owner=pro)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    me = user.email

    f = File.objects.get(pk=pk)
    newname = request.POST.get('popup-input-q','')
    if newname == '':
        warningmsg = 'enter a name'
        context = {"storagevalue":storagevalue,"parent":pf,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'alert':1, 'warningmsg':warningmsg, 'all_folder_list':all_folder_list}
        return render(request, 'uploads/subfolder.html', context)
    oldname = f.name
    f.name = newname +'.'+f.file_type
    f.name = newname
    successmsg = 'renamed file ' + oldname + ' to file ' + f.name
    f.save()

    context = getcontexttrash(request)
    context.update({"successmsg":successmsg})
    context.update({"successalert":1})
    f.save()

    image_list = pf.folderfiles.all()
    context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list, 'folder_list':folder_list, 'me':me, 'storage':storage, "parent":pf}

    return render(request, 'uploads/subfolder.html', context)

#displays one selected file
@login_required(login_url='/users/login/')
def file(request, slug,fid):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = user.id
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    storage = getstorage(pro)
    storagevalue = pro.storage
    all_folder_list = Folder.objects.filter(owner=pro)
    f = File.objects.get(pk=fid)
    instance = f
    object_viewed_signal.send(instance.__class__,instance=instance,request=request)
    image_list = []
    image_list.append(f)
    context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list,'all_folder_list':all_folder_list, 'storage':storage,'instance':instance}
    return render(request, 'uploads/my-drive.html', context)

def findfile(request, pk):
    user = request.user
    pro = Profile.objects.get(user=user)
    storagevalue = pro.storage
    email = user.email
    uid = user.id
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    storage = getstorage(pro)
    all_folder_list = Folder.objects.filter(owner=pro)
    f = File.objects.get(pk=pk)
    instance = f
    object_viewed_signal.send(instance.__class__,instance=instance,request=request)
    image_list = []
    image_list.append(f)
    context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list,'all_folder_list':all_folder_list, 'storage':storage,'instance':instance}
    return render(request, 'uploads/my-drive.html', context)

#renames a root folder
@csrf_exempt
@login_required(login_url='/users/login/')
def renamefolder(request, slug, pk):

   
    f = Folder.objects.get(pk=pk)
    newname = request.POST.get('popup-input-q','') 
    if newname == '':
        warningmsg = 'enter a name'
        context = getcontext(request)
        context.update({"warningmsg":warningmsg})
        context.update({"alert":1})
        return render(request, 'uploads/my-drive.html', context)
    f.name = newname
    f.save()

    context = getcontext(request)

    return render(request, 'uploads/my-drive.html', context)


#renames a root folder
@csrf_exempt
@login_required(login_url='/users/login/')
def renamefoldertable(request, slug, pk):

    
    f = Folder.objects.get(pk=pk)
    newname = request.POST.get('popup-input-q','')
    if newname == '':
        warningmsg = 'enter a folder name'
        context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'alert':1, 'warningmsg':warningmsg, 'all_folder_list':all_folder_list}
        return render(request, 'uploads/my-drive-table-old.html', context)
    f.name = newname
    f.save()

    context = getcontext(request)


    return render(request, 'uploads/my-drive-table-old.html', context)


@csrf_exempt
@login_required(login_url='/users/login/')
def renamefoldertabletrash(request, slug, pk):

   
    f = Folder.objects.get(pk=pk)
    newname = request.POST.get('popup-input-q','')
    if newname == '':
        warningmsg = 'enter a folder name'
        context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'alert':1, 'warningmsg':warningmsg, 'all_folder_list':all_folder_list}
        return render(request, 'uploads/my-drive-table-old.html', context)
    f.name = newname
    f.save()

    context = getcontexttrash(request)
    return render(request, 'uploads/my-drive-table-trash.html', context)
#renames a starred root folder
@csrf_exempt
@login_required(login_url='/users/login/')
def renamefolderstar(request, slug, pk):

  
    f = Folder.objects.get(pk=pk)
    newname = request.POST.get('popup-input-q','')
    if newname == '':
        warningmsg = 'enter a folder name'
        context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'alert':1, 'warningmsg':warningmsg, 'all_folder_list':all_folder_list}
        return render(request, 'uploads/my-drive-star.html', context)
    f.name = newname
    f.save()

    context = getcontextstar(request)

    return render(request, 'uploads/my-drive-star.html', context)


@csrf_exempt
@login_required(login_url='/users/login/')
def renamefolderstartable(request, slug, pk):

    
    f = Folder.objects.get(pk=pk)
    newname = request.POST.get('popup-input-q','')
    f.name = newname
    f.save()

    getcontextstar(request)

    return render(request, 'uploads/my-drive-table-star.html', context)

@csrf_exempt
@login_required(login_url='/users/login/')
def renamefoldertrash(request, slug, pk):

   
    f = Folder.objects.get(pk=pk)
    newname = request.POST.get('popup-input-q','')
    f.name = newname
   
    f.save()

    return render(request, 'uploads/my-drive-trash.html', context)
#renames a child folder
@csrf_exempt
@login_required(login_url='/users/login/')
def renamesubfolder(request, slug, pk):

    user = request.user
    pro = Profile.objects.get(user=user)
    storagevalue = pro.storage
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    pf = Folder.objects.get(id=request.session['fid'])
    storagemb = getstoragemb(pro)
    storage = getstorage(pro)
    all_folder_list = Folder.objects.filter(owner=pro)
    me = user.email

    f = Folder.objects.get(pk=pk)
    newname = request.POST.get('popup-input-q','')
    f.name = newname
    f.save()
    folder_list = Folder.objects.filter(parent=pf)
    image_list = pf.folderfiles.all()
    context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list,  'folder_list':folder_list, 'storage':storage, 'all_folder_list':all_folder_list,"parent":f}

    return render(request, 'uploads/subfolder.html', context)


@login_required(login_url='/users/login/')
@csrf_exempt
def share(request, slug, pk):
    context = getcontext(request)
    sharewith = request.POST.get('popup-input-q','')
    if sharewith == '':
        warningmsg = 'enter a user'
        context = getcontext(request)
        context.update({"warningmsg":warningmsg})
        context.update({"alert":1})
        return render(request, 'uploads/my-drive.html', context)
    exists = CustomUser.objects.filter(email=sharewith)
    sharepro = None
    if(exists):
        sharepro = Profile.objects.get(user=exists[0])
        f = File.objects.get(pk=pk)
        sharepro.sharedfiles.add(f)
        sharepro.save()
        successmsg = 'shared with ' + sharewith
        context.update({'successmsg':successmsg})
        context.update({'successalert':1})
    else:
        warningmsg = sharewith + ' is not a user'
        context.update({'warningmsg':warningmsg})
        context.update({'alert':1})

    return render(request, 'uploads/my-drive.html', context)

@login_required(login_url='/users/login/')
@csrf_exempt
def sharefolder(request, slug, pk):
    context = getcontext(request)
    sharewith = request.POST.get('popup-input-q','')
    if sharewith == '':
        warningmsg = 'enter a user'
        context = getcontext(request)
        context.update({"warningmsg":warningmsg})
        context.update({"alert":1})
        return render(request, 'uploads/my-drive.html', context)
    exists = CustomUser.objects.filter(email=sharewith)
    sharepro = None
    if(exists):
        sharepro = Profile.objects.get(user=exists[0])
        f = Folder.objects.get(pk=pk)
        sharepro.sharedfolders.add(f)
        sharepro.save()
        successmsg = 'shared with ' + sharewith
        context.update({'successmsg':successmsg})
        context.update({'successalert':1})
    else:
       warningmsg = sharewith + ' is not a user'
       context.update({'warningmsg':warningmsg})
       context.update({'alert':1})

    return render(request, 'uploads/my-drive.html', context)



@login_required(login_url='/users/login/')
def sharedwithme(request):
    user = request.user
    pro = Profile.objects.get(user=user)
    storagevalue = pro.storage
    email = user.email
    cuser = User.objects.get(id=user.id)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    all_files = pro.sharedfiles.all()
    all_folders = pro.sharedfolders.all()
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    image_list = []
    folder_list = []
    for fi in all_files:
        image_list.append(fi)
    for fi in all_folders:
        folder_list.append(fi)
    context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"image_list":image_list, 'storage':storage, 'storagemb':storagemb,'folder_list':folder_list}
    return render(request, 'uploads/my-drive.html', context)

#move file
@csrf_exempt
@login_required(login_url='/users/login/')
def moveto(request, slug, pk, fk):
    user = request.user
    pro = Profile.objects.get(user=user)
    storagevalue = pro.storage
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)

    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    all_folder_list = Folder.objects.filter(owner=pro)
    f = Folder.objects.get(pk=fk)
    fi = File.objects.get(pk=pk)
    fold = Folder.objects.all()
    for fo in fold:
        objs = fo.folderfiles.all()
        for obj in objs:
            if(obj == fi):
                if(obj.owner == fi.owner):
                    fo.folderfiles.remove(obj)

    #add file to folder
    fi.folder = f
    fi.save()
    f.folderfiles.add(fi)
    f.save()

    #how much memory the user has remaining
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)

    #check if file is moved to genesis folder
    if(pro.gid == f.id):
        image_list = File.objects.filter(owner=pro)
        folder_list = None
        if pro.gid != 0:
            g = Folder.objects.get(id=pro.gid)
            folder_list = Folder.objects.filter(parent=g)
        qa_list = []
        x = 0

        for image in image_list:
            if 'jpeg' or 'png' or 'jpg' in image.file_type:
                x = x + 1
                if x == 20:
                    return render(request, 'uploads/my-drive.html', context)
                qa_list.append(image)
                context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"all_folder_list":all_folder_list,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list, 'storage':storage,'storagemb':storagemb}


        context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"all_folder_list":all_folder_list,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list, 'storage':storage,'storagemb':storagemb, 'all_folder_list':all_folder_list}
        return render(request, 'uploads/my-drive.html', context)

    #file is moved to subfolder
    else:
        f = Folder.objects.get(id=fk)
        folder_list = Folder.objects.filter(parent=f)
        image_list = f.folderfiles.all()
        all_folder_list = Folder.objects.filter(owner=pro)
        context = {"email":email,"firstinitial":firstinitial,"name":name,"all_folder_list":all_folder_list,"image_list":image_list,  'folder_list':folder_list, 'storage':storage,'storagemb':storagemb, 'all_folder_list':all_folder_list,"parent":f}
        return render(request, 'uploads/subfolder.html', context)

#move folder
@login_required(login_url='/users/login/')
def movefolderto(request, slug, pk, fk):
    user = request.user
    pro = Profile.objects.get(user=user)

    #parent folder is the destination
    p = Folder.objects.get(pk=fk)
    parentpath = p.path

    #child folder is the source
    c = Folder.objects.get(pk=pk)
    childpath = c.path
    
    #set childs parents to the destination
    c.parent = p
    p.children.add(c)


    #save

    c.save()
    p.save()
    
    genesis = getgenesis(pro)
   
    dirwalk(pro,c,p)
  
    
    shutil.move(childpath, parentpath) 

    context = getcontext(request)
    return render(request, 'uploads/my-drive.html', context)


#creates genesis folder if it is the first folder created
@csrf_exempt
@login_required(login_url='/users/login/')
def firstfolder(request):
    user = request.user
    pro = Profile.objects.get(user=user)

    path = BASE_DIR+'/media/'+ str(user)
    if pro.gid == 0:
        os.chdir(path)
        os.mkdir('genesis')
        path += '/genesis/'
        g = Folder.objects.create(path = path, owner=pro, name='genesis')

        os.chdir(path)
        f = Folder.objects.create(path = path+foldername, owner=pro, name=foldername, parent=g)
        os.mkdir(foldername)
        g.children.add(f)
        g.save()

        pro.gid = g.id
        pro.save()

        return 1
    else:

        return 0



@csrf_exempt

#makes the created folder a child of the genesis folder
@login_required(login_url='/users/login/')
def rootfolder(request):
    user = request.user
    pro = Profile.objects.get(user=user)
    storagevalue = pro.storage
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    image_list = File.objects.filter(owner=pro)
    all_folder_list = Folder.objects.filter(owner=pro)
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g,trash=False)
    qa_list = []
    x = 0

    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                break
            qa_list.append(image)
    all_folder_list = Folder.objects.filter(owner=pro)


    foldername = request.POST.get('newfolder-q','')
    if foldername == '':
        warningmsg = 'enter a folder name'
        context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'qa_list':qa_list, 'alert':1, 'warningmsg':warningmsg, 'all_folder_list':all_folder_list}
        return render(request, 'uploads/my-drive.html', context)
    path = BASE_DIR+'/media/accounts/'+ str(user)
    if pro.gid == 0:
        if os.path.exists(path):
            os.chdir(path)
        else:
            os.makedirs(path,exist_ok=True)
            os.chdir(path)
        path += '/genesis/'
        if not os.path.exists(path):
            os.mkdir('genesis')
        g = Folder.objects.create(path = path, owner=pro, name='genesis')

        duplicatenamecheck = Folder.objects.filter(name=foldername, owner=pro, parent=g)
        if(duplicatenamecheck):
            warningmsg = foldername + ' already exists'
            context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'qa_list':qa_list, 'alert':1, 'warningmsg':warningmsg, 'all_folder_list':all_folder_list}
            return render(request, 'uploads/my-drive.html', context)

     

        os.chdir(path)
        f = Folder.objects.create(path = path+foldername+'/', owner=pro, name=foldername, parent=g)
        os.mkdir(foldername)
        g.children.add(f)
        g.save()

        pro.gid = g.id
        pro.save()
    else:
        g = Folder.objects.get(id=pro.gid)



        duplicatenamecheck = Folder.objects.filter(name=foldername, owner=pro, parent=g)
        if(duplicatenamecheck):
            warningmsg = foldername + ' already exists'
            context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'qa_list':qa_list, 'alert':1, 'warningmsg':warningmsg, 'all_folder_list':all_folder_list}
            return render(request, 'uploads/my-drive.html', context)
       
        f = Folder.objects.create(path = g.path+foldername+'/', owner=pro, name=foldername, parent=g)
        os.chdir(g.path)
        os.mkdir(foldername)
        g.children.add(f)
        g.save()


    image_list = File.objects.filter(owner=pro)
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g,trash=False)
    qa_list = []
    x = 0
    successmsg = foldername + ' created'
    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                return render(request, 'uploads/my-drive.html', context)
            qa_list.append(image)
            context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,'successalert':1,"successmsg":successmsg,"all_folder_list":all_folder_list,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list, 'storage':storage}


    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"successmsg":successmsg,"all_folder_list":all_folder_list,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list, 'storage':storage, 'successalert':1,'foldername':foldername}
    return render(request, 'uploads/my-drive.html', context)

@login_required(login_url='/users/login/')
def subfolder(request, pk):
    request.session['fid'] = pk
    user = request.user
    pro = Profile.objects.get(user=user)
    storagevalue = pro.storage
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    f = Folder.objects.get(id=pk)
    folder_list = Folder.objects.filter(parent=f)
    image_list = f.folderfiles.all()
    all_folder_list = Folder.objects.filter(owner=pro)
    context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list,  'folder_list':folder_list, 'storage':storage, 'all_folder_list':all_folder_list,"parent":f}
    return render(request, 'uploads/subfolder.html', context)


#makes the created folder a child of its direct parent
@csrf_exempt
@login_required(login_url='/users/login/')
def makesubfolder(request):
    pf = Folder.objects.get(id=request.session['fid'])
    user = request.user
    pro = Profile.objects.get(user=user)
    storagevalue = pro.storage
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    all_folder_list = Folder.objects.filter(owner=pro)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    image_list = pf.folderfiles.all()
    folder_list = Folder.objects.filter(parent=pf)

    foldername = request.POST.get('newsubfolder-q','')
    if foldername == '':
        warningmsg = 'enter a folder name'
        context = {"storagevalue":storagevalue,"alert":1,"warningmsg":warningmsg,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'foldername':foldername, 'parent':pf}
        return render(request, 'uploads/subfolder.html', context)


    duplicatenamecheck = Folder.objects.filter(name=foldername, owner=pro, parent=pf)
   
    if(duplicatenamecheck):
        warningmsg = foldername + ' already exists'
        context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"warningmsg":warningmsg,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'alert':1, 'foldername':foldername, 'parent':pf}
        return render(request, 'uploads/subfolder.html', context)
    sf = Folder.objects.create(parent=pf, owner=pro, name=foldername, path=pf.path+'/'+foldername+'/')
    os.chdir(pf.path)
    os.mkdir(foldername)
    pf.children.add(sf)
    pf.save()
    successmsg = 'subfolder ' + sf.name + ' created';
    folder_list = Folder.objects.filter(parent=pf)
    context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'foldername':foldername, 'parent':pf,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/subfolder.html', context)

@login_required(login_url='/users/login/')
def dupfilecheck(pro, fname, copynum):

    #check if filename exists for given user
    copycheck = File.objects.filter(owner=pro, name=fname)

    oldname = None
    if(copycheck):
        #file name exists 
        #save original filename
        oldname = fname

        #add copy number
        fname = fname.replace(str(copynum),'')
        fname = fname.replace('()','')
        split = fname.split(".")
        copynum += 1
        if len(split) > 1:
            fname = split[0] + '(' + str(copynum) + ').' + split[1]
        else:
            fname = split[0] + '(' + str(copynum) + ')'
        return dupfilecheck(pro, fname, copynum)
    else:
        #file name is unique return true and filename
        return 1, fname, oldname


@login_required(login_url='/users/login/')
def dupfoldercheck(pro, fname, copynum):

    #check if filename exists for given user
    copycheck = Folder.objects.filter(owner=pro, name=fname)


    if(copycheck):
        #file name exists add copy number
        fname = fname.replace(str(copynum),'')
        fname = fname.replace('()','')
        split = fname.split(".")
        copynum += 1
        fname = fname + '(' + str(copynum) + ')'
        return dupfoldercheck(pro, fname, copynum)
    else:
        #file name is unique return true and filename
        return 1, fname



@csrf_exempt
@login_required(login_url='/users/login/')
def copyfile(request,slug,pk):
    pro = Profile.objects.get(user=request.user)
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    if len(fname) > 1:
        newfilename = fname[0] + 'copy.' + fname[1]
    else:
        newfilename = fname[0] + 'copy'
        fname.append('')

    copynum = 0
    x,y, tmp = dupfilecheck(pro,newfilename,copynum)
    #check if a copy of the file
    if(dupfilecheck(pro,newfilename,copynum)):
        filecopypath = f.path.replace(f.name,y)
        filecopy = File.objects.create(owner=f.owner,name=y,path=filecopypath,file_type=fname[1].lower(),size=f.size)
        dest = shutil.copyfile(BASE_DIR+f.path, BASE_DIR+filecopypath) 


        filecopy.save()
        pro.storage += float(filecopy.size)
        pro.save()
        successmsg = 'created ' + filecopy.name

    context = getcontext(request)
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})
    return render(request, 'uploads/my-drive.html', context)


@csrf_exempt
@login_required(login_url='/users/login/')
def copyfiletrash(request,slug,pk):
    pro = Profile.objects.get(user=request.user)
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    if len(fname) > 1:
        newfilename = fname[0] + 'copy.' + fname[1]
    else:
        newfilename = fname[0] + 'copy'
        fname.append('')

    copynum = 0
    x,y, tmp = dupfilecheck(pro,newfilename,copynum)
    #check if a copy of the file
    if(dupfilecheck(pro,newfilename,copynum)):
        filecopypath = f.path.replace(f.name,y)
        filecopy = File.objects.create(owner=f.owner,name=y,path=filecopypath,file_type=fname[1].lower(),size=f.size,trash=True)
        dest = shutil.copyfile(BASE_DIR+f.path, BASE_DIR+filecopypath) 
        filecopy.save()
        pro.storage += float(filecopy.size)
        pro.save()
        successmsg = 'created ' + filecopy.name

    context = getcontexttrash(request)
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})
    return render(request, 'uploads/my-drive-trash.html', context)


@csrf_exempt
@login_required(login_url='/users/login/')
def copyfiletrashtable(request,slug,pk):
    user = request.user
    pro = Profile.objects.get(user=user)
    storagevalue = pro.storage
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    image_list = File.objects.filter(owner=pro,trash=True)
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g,trash=True)
    qa_list = []
    x = 0

    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                break
            qa_list.append(image)
    all_folder_list = Folder.objects.filter(owner=pro)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    if len(fname) > 1:
        newfilename = fname[0] + 'copy.' + fname[1]
    else:
        newfilename = fname[0] + 'copy'
        fname.append('')

    copynum = 0
    x,y, tmp = dupfilecheck(pro,newfilename,copynum)
   
    #check if a copy of the file
    if(dupfilecheck(pro,newfilename,copynum)):
        filecopypath = f.path.replace(f.name,y)
        filecopy = File.objects.create(owner=f.owner,name=y,path=filecopypath,file_type=fname[1].lower(),size=f.size,trash=True)
        dest = shutil.copyfile(BASE_DIR+f.path, BASE_DIR+filecopypath)        
        filecopy.save()
        pro.storage += float(filecopy.size)
        pro.save()
        successmsg = 'created ' + filecopy.name

    image_list = File.objects.filter(owner=pro,trash=True)
    context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/my-drive-table-trash.html', context)

@csrf_exempt
@login_required(login_url='/users/login/')
def copyfiletable(request,slug,pk):
    pro = Profile.objects.get(user=request.user)
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    if len(fname) > 1:
        newfilename = fname[0] + 'copy.' + fname[1]
    else:
        newfilename = fname[0] + 'copy'
        fname.append('')

    copynum = 0
    x,y, tmp = dupfilecheck(pro,newfilename,copynum)
   
    #check if a copy of the file
    if(dupfilecheck(pro,newfilename,copynum)):
        filecopypath = f.path.replace(f.name,y)
        filecopy = File.objects.create(owner=f.owner,name=y,path=filecopypath,file_type=fname[1].lower(),size=f.size)
        dest = shutil.copyfile(BASE_DIR+f.path, BASE_DIR+filecopypath)       
        filecopy.save()
        pro.storage += float(filecopy.size)
        pro.save()
        successmsg = 'created ' + filecopy.name

    context = getcontext(request)
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})
    return render(request, 'uploads/my-drive-table-old.html', context)


@csrf_exempt
@login_required(login_url='/users/login/')
def copystarfile(request,slug,pk):
    user = request.user
    pro = Profile.objects.get(user=user)
    storagevalue = pro.storage
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    image_list = File.objects.filter(owner=pro,starred=True)
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g,starred=True)
    qa_list = []
    x = 0

    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                break
            qa_list.append(image)
    all_folder_list = Folder.objects.filter(owner=pro,starred=True)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    if len(fname) > 1:
        newfilename = fname[0] + 'copy.' + fname[1]
    else:
        newfilename = fname[0] + 'copy'
        fname.append('')

    copynum = 0
    x,y, tmp = dupfilecheck(pro,newfilename,copynum)
    
    #check if a copy of the file
    if(dupfilecheck(pro,newfilename,copynum)):
        filecopypath = f.path.replace(f.name,y)
        filecopy = File.objects.create(owner=f.owner,name=y,path=filecopypath,file_type=fname[1].lower(),size=f.size,starred=True)
        dest = shutil.copyfile(BASE_DIR+f.path, BASE_DIR+filecopypath)       
        filecopy.save()
        pro.storage += float(filecopy.size)
        pro.save()
        successmsg = 'created ' + filecopy.name

    image_list = File.objects.filter(owner=pro,starred=True)
    context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/my-drive-star.html', context)

@csrf_exempt
@login_required(login_url='/users/login/')
def copystarfiletable(request,slug,pk):
    user = request.user
    pro = Profile.objects.get(user=user)
    storagevalue = pro.storage
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    image_list = File.objects.filter(owner=pro,starred=True)
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g,starred=True)
    qa_list = []
    x = 0

    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                break
            qa_list.append(image)
    all_folder_list = Folder.objects.filter(owner=pro,starred=True)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    if len(fname) > 1:
        newfilename = fname[0] + 'copy.' + fname[1]
    else:
        newfilename = fname[0] + 'copy'
        fname.append('')

    copynum = 0
    x,y, tmp = dupfilecheck(pro,newfilename,copynum)
  
    #check if a copy of the file
    if(dupfilecheck(pro,newfilename,copynum)):
        filecopypath = f.path.replace(f.name,y)
        filecopy = File.objects.create(owner=f.owner,name=y,path=filecopypath,file_type=fname[1].lower(),size=f.size,starred=True)
        dest = shutil.copyfile(BASE_DIR+f.path, BASE_DIR+filecopypath)         
        filecopy.save()
        pro.storage += float(filecopy.size)
        pro.save()
        successmsg = 'created ' + filecopy.name

    image_list = File.objects.filter(owner=pro,starred=True)
    context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/my-drive-table-star.html', context)





@login_required(login_url='/users/login/')
def dirwalktrash(pro, pk):
    #pf = current folder
    pf = pk
    gid = pro.gid
    gf = Folder.objects.get(id=gid)
    children = pf.children.all()
    gen = getgenesis(pro)
    
    pf.trash = True

    if pf.folderfiles:
        
        files = pf.folderfiles.all()
        #update the path of the files in the folder
        for f in files:
            f.trash = True
            f.save()
    for child in children:
        if child.id == pf.parent.id:
            #this is the parent id
            pass
        elif child.id == gf.id:
            #this is the genesis folder
            pass
        else:
            dirwalktrash(pro, child)
                
    return

@login_required(login_url='/users/login/')
def dirwalkdelete(pro, pk):
    #pf = current folder
    pf = pk
    gid = pro.gid
    gf = Folder.objects.get(id=gid)
    children = pf.children.all()
    gen = getgenesis(pro)
    
   

    if pf.folderfiles:
        
        files = pf.folderfiles.all()
        #update the path of the files in the folder
        for f in files:
            pro.storage -= float(f.size)
            pro.save()
            f.delete()
    for child in children:
        if child.id == pf.parent.id:
            #this is the parent id
            pass
        elif child.id == gf.id:
            #this is the genesis folder
            pass
        else:
            dirwalkdelete(pro, child)
                
    return

@login_required(login_url='/users/login/')
def dirwalk(pro, pk, dst):
    #pf = current folder
    pf = pk
    gid = pro.gid
    gf = Folder.objects.get(id=gid)
    children = pf.children.all()
    gen = getgenesis(pro)
    pf.path = dst.path + '/' + pf.path.replace(gen,'')
    pf.save()
    if pf.folderfiles:
        files = pf.folderfiles.all()
        #update the path of the files in the folder
        for f in files:
            f.path = pf.path + '/' + f.name
            f.path = f.path.replace(BASE_DIR,'')
           #f.file.name = f.path
            f.save()
    for child in children:
        if child.id == pf.parent.id:
            #this is the parent id
            pass
        elif child.id == dst.id:
            #this is the dst
            pass
        elif child.id == gf.id:
            #this is the genesis folder
            pass
        else:
            dirwalk(pro, child, dst)
    return


@login_required(login_url='/users/login/')
def dirwalkcopyfolder(pro, pk, argparent):
    #pf = current folder
    pf = pk
    gid = pro.gid
    gf = Folder.objects.get(id=gid)
    children = pf.children.all()
    gen = getgenesis(pro)
    x,copyname = dupfoldercheck(pro,pf.name,0)

    parentcopy = Folder.objects.create(owner=pf.owner,name=copyname,parent=argparent,path=argparent.path)
    parentcopy.path += parentcopy.name + '/'
    parentcopy.save()
    os.mkdir(parentcopy.path)

    if pf.folderfiles:
        files = pf.folderfiles.all()
        #update the path of the files in the folder
        for f in files:
            x,copyname,tmp = dupfilecheck(pro,f.name,0)
 
            filecopy = File.objects.create(owner=f.owner,name=copyname,path=pf.path+'/'+f.name,size=f.size,file_type=f.file_type)
            #format path for media
            filecopy.path = filecopy.path.replace(BASE_DIR,'')
            filecopy.save()
            pro.storage += float(f.size)
            pro.save()
            parentcopy.folderfiles.add(filecopy)
            pf.save()
            shutil.copyfile(pf.path+'/'+f.name,parentcopy.path+'/'+copyname)


    for child in children:
        if child.id == pf.parent.id:
            #this is the parent id
            pass
      
        elif child.id == gf.id:
            #this is the genesis folder
            pass
        else:
            dirwalkcopyfolder(pro,child,parentcopy)
    return

@login_required(login_url='/users/login/')
def dirwalkstar(pro, pk, argparent):
    #pf = current folder
    pf = pk
    gid = pro.gid
    gf = Folder.objects.get(id=gid)
    children = pf.children.all()
    gen = getgenesis(pro)
    x,copyname = dupfoldercheck(pro,pf.name,0)

    parentcopy = Folder.objects.create(owner=pf.owner,name=copyname,parent=argparent,path=argparent.path,starred=True)
    parentcopy.path += parentcopy.name + '/'
    parentcopy.save()

    if pf.folderfiles:
        files = pf.folderfiles.all()
        #update the path of the files in the folder
        for f in files:
            x,copyname,tmp = dupfilecheck(pro,f.name,0)
 
            filecopy = File.objects.create(owner=f.owner,name=copyname,path=pf.path+'/'+f.name,size=f.size,file_type=f.file_type,starred=True)
            #format path for media
            filecopy.path = filecopy.path.replace(BASE_DIR,'')
            filecopy.save()
            pro.storage += float(filecopy.size)
            pro.save()
            parentcopy.folderfiles.add(filecopy)
            pf.save()


    for child in children:
        if child.id == pf.parent.id:
            #this is the parent id
            pass
      
        elif child.id == gf.id:
            #this is the genesis folder
            pass
        else:
            dirwalkstar(pro,child,parentcopy)
    return


@login_required(login_url='/users/login/')
def copyfolderview(request,slug,pk):
    pro = Profile.objects.get(user=request.user)
    f = Folder.objects.get(pk=pk)
    dirwalkcopyfolder(pro, f,f.parent)
    successmsg = 'copied folder ' + f.name
    context = getcontext(request)
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})
    return render(request, 'uploads/my-drive.html', context)

@login_required(login_url='/users/login/')
def copyfoldertableview(request,slug,pk):
    pro = Profile.objects.get(user=request.user)
    f = Folder.objects.get(pk=pk)
    dirwalkcopyfolder(pro, f,f.parent)
    successmsg = 'copied folder ' + f.name
    context = getcontext(request)
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})
    return render(request, 'uploads/my-drive-table-old.html', context)

@login_required(login_url='/users/login/')
def copystarfolderview(request,slug,pk):
    pro = Profile.objects.get(user=request.user)
    f = Folder.objects.get(pk=pk)
    dirwalkstar(pro, f,f.parent)
    successmsg = 'copied folder ' + f.name
    context = getcontextstar(request)
    context.update({"successmsg":successmsg})
    context.update({"successalert":1})
    return render(request, 'uploads/my-drive-star.html', context)

@login_required(login_url='/users/login/')
def copystarfoldertableview(request,slug,pk):
    pro = Profile.objects.get(user=request.user)
    f = Folder.objects.get(pk=pk)
    dirwalkstar(pro, f,f.parent)
    successmsg = 'copied folder ' + f.name
    context = getcontextstar(request)
    context.update({"successmsg":successmsg})
    context.update({"successalert":1})
    return render(request, 'uploads/my-drive-table-star.html', context)

@login_required(login_url='/users/login/')
def copytrashfolderview(request,slug,pk):
    pro = Profile.objects.get(user=request.user)
    f = Folder.objects.get(pk=pk)
    dirwalktrash(pro, f,f.parent)
    successmsg = 'copied folder ' + f.name
    context = getcontexttrash(request)
    context.update({"successmsg":successmsg})
    context.update({"successalert":1})
    return render(request, 'uploads/my-drive-trash.html', context)


@login_required(login_url='/users/login/')
def copytrashfoldertableview(request,slug,pk):
    pro = Profile.objects.get(user=request.user)
    f = Folder.objects.get(pk=pk)
    dirwalktrash(pro, f,f.parent)
    successmsg = 'copied folder ' + f.name
    context = getcontexttrash(request)
    context.update({"successmsg":successmsg})
    context.update({"successalert":1})
    return render(request, 'uploads/my-drive-table-trash.html', context)

@login_required(login_url='/users/login/')
def copysubfile(request,slug,pk):
    user = request.user
    pro = Profile.objects.get(user=user)
    storagevalue = pro.storage
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    pf = Folder.objects.get(id=request.session['fid'])
    folder_list = Folder.objects.filter(parent=pf)
    image_list = pf.folderfiles.all()
    
    all_folder_list = Folder.objects.filter(owner=pro)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    newfilename = fname[0] + 'copy.' + fname[1]
   

    copynum = 0
    x,y, tmp = dupfilecheck(pro,newfilename,copynum)
   
    #check if a copy of the file
    if(dupfilecheck(pro,newfilename,copynum)):
        filecopy = File.objects.create(owner=f.owner,name=y,path=f.path,file_type=fname[1].lower(),size=f.size)
        filecopy.save()
        pf.folderfiles.add(filecopy)
        pf.save()
        successmsg = 'created' + filecopy.name

    image_list = pf.folderfiles.all()
    context = {"storagevalue":storagevalue,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage,'successalert':1,'successmsg':successmsg,"parent":pf}

    return render(request, 'uploads/subfolder.html', context)






login_required(login_url='/users/login/')
def download(request, slug, pk):
    f = File.objects.get(id=pk)
    user = request.user
    pro = Profile.objects.get(user=user)
    path = BASE_DIR + f.path
    f0 = open(path, 'rb')
    myfile = DjangoFile(f0)
    response = HttpResponse(myfile)
    response['Content-Disposition'] = 'attachment; filename=' + f.name
    return response






def downloadfolder(request, slug, pk):
    f = Folder.objects.get(id=pk)
    pro = Profile.objects.get(user=request.user)
    genesis = getgenesis(pro)
  
    shutil.make_archive(f.path, 'zip',f.path)
    f0 = open('/'+f.path.strip("/")+'.zip', 'rb')
    myfile = DjangoFile(f0)

    #might remove files from folder after zip is created

    response = HttpResponse(myfile)
    response['Content-Disposition'] = 'attachment; filename=' + f.name+'.zip'
    return response



@csrf_exempt
def searchajax(request):
    user = request.user
    pro = Profile.objects.get(user=user)
    searchq = request.GET.get('searchq', None)
    if request.method == "POST":
        searchq = request.POST['searchq']
    f_json = False
    if(File.objects.filter(name__contains=searchq).exists()):
            f = File.objects.filter(name__contains=searchq, owner=pro)

    data = {
        'is_taken': f_json
    }
    return render(None,'uploads/ajax_search.html', {'files':f})








@csrf_exempt
def upload_driver(request):
    upload_file = request.FILES['drive_file']
   
    pro = Profile.objects.get(user=request.user)

    ret = {}
    if upload_file:
        
        if not checkstorage(pro,upload_file.size):
            return HttpResponse(status=406)

        target_folder = BASE_DIR+'/media/accounts/'+str(request.user)+'/genesis/'
        if not os.path.exists(target_folder): os.mkdir(target_folder)
        rtime = str(int(time.time()))
        #remove whitespace from filenames
        filename = request.POST['filename'].replace(" ","")
        ftype = filename.split('.')[-1]
        target = os.path.join(target_folder, filename)
        gf = Folder.objects.get(id=pro.gid)
        f = File.objects.create(owner=pro, name=filename.strip(), file_type=ftype.lower(),path='/media/accounts/'+str(request.user)+'/genesis/'+filename)
        ret = {"file":f.path,"id":f.id,"name":filename,"filetype":f.file_type}
        gf.folderfiles.add(f)
        f.save()
        gf.save()
        with open(target, 'wb+') as dest:
          for c in upload_file.chunks():
            dest.write(c)

        if os.path.getsize(target):
            size = os.path.getsize(target)
        else:
            size = 0   
        f.size = size
        f.save()
        pro.storage += f.size
        pro.save()   
        ret['file_remote_path'] = target
    else:
        return HttpResponse(status=500)
    return HttpResponse(json.dumps(ret))


@csrf_exempt
def sub_upload_driver(request):
    pro = Profile.objects.get(user=request.user)
    if 'drive_file' in request.FILES:
        upload_file = request.FILES['drive_file']
    else:
        upload_file = None
    if 'fid' in request.session:
                pk = request.session['fid']
                pf = Folder.objects.get(id=pk)
    ret = {}
    if upload_file:

        if not checkstorage(pro,upload_file.size):
            return HttpResponse(status=406)
        target_folder = pf.path + '/'
        if not os.path.exists(target_folder): os.mkdir(target_folder)
        rtime = str(int(time.time()))
        #remove whitespace from filenames
        filename = request.POST['filename'].strip()
        
        target = os.path.join(target_folder, filename)
        ftype = filename.split('.')[-1]
        fpath = pf.path.replace(BASE_DIR,'')
        f = File.objects.create(file_type=ftype.lower(),owner=pro, name=filename, path=fpath+'/'+filename)
        ret = {"file":f.path,"id":f.id,"name":filename,"filetype":f.file_type}
        pf.folderfiles.add(f)
        f.save()
        pf.save()
        with open(target, 'wb+') as dest:
          for c in upload_file.chunks():
            dest.write(c)

        if os.path.getsize(target):
            size = os.path.getsize(target)
        else:
            size = 0   
        f.size = size
        f.save()
        pro.storage += f.size
        pro.save()   
        ret['file_remote_path'] = target
    else:
        return HttpResponse(status=500)
    return HttpResponse(json.dumps(ret))

@csrf_exempt
def createfolders(pro,apath):
    
    everyfilepath = apath
    ret = {}
    directories = []
    gpath = getgenesis(pro)
    if everyfilepath:
        #separate every filepath into a list element 
       
       
        for pathindex, path in enumerate(everyfilepath):
            

            dirlist = path.split('/')
            fname = dirlist.pop()
            fullpath = gpath+path.replace(fname,'')
            if os.path.exists(fullpath):
                pass
            else:
                os.makedirs(fullpath)
            directories.append(dirlist)
        #remove duplicate folders to create database structure
        dirset = set()   
        for mydir in directories:
            dirset.add(tuple(mydir))

        dirlist = []
        for item in dirset:
            dirlist.append(list(item))

        g = Folder.objects.get(id=pro.gid)
        for mdir in dirlist:
            parentf = None
            if len(mdir) == 1:
                if Folder.objects.filter(name=str(mdir[0]),owner=pro).exists():
                    pass
                else:
                    f = Folder.objects.create(name=str(mdir[0]), parent=g,owner=pro)
                g.children.add(f)
                g.save()

            else:

                i = 0
                temp = None
                while i < len(mdir):
                    if i == 0:
                        if Folder.objects.filter(name=str(mdir[i]),owner=pro).exists():
                            temp = Folder.objects.filter(name=str(mdir[i]), owner=pro)[0]
                        else:
                            f = Folder.objects.create(name=str(mdir[i]), parent=g,owner=pro)
                            temp = f
                            g.children.add(f)
                            g.save()
                    else:
                        if Folder.objects.filter(name=str(mdir[i]), owner=pro).exists():
                            temp = Folder.objects.filter(name=str(mdir[i]), owner=pro)[0]
                        else:
                            f = Folder.objects.create(name=str(mdir[i]), parent=temp,owner=pro)
                            temp.children.add(f)
                            temp.save()
                            temp = f
                    i += 1 
    return 





@csrf_exempt
def files_upload(request):
    d = {}
    resplist = []
    pro = Profile.objects.get(user=request.user)
    genesis = getgenesis(pro)
    UPLOAD_PATH = BASE_DIR + genesis
    if request.method == 'GET':
        return render(request, 'uploads/my-drive.html',{})
    elif request.is_ajax(): 
        # The file object to take name attribute value input box
        files = request.FILES.getlist('files')
        fpaths = request.POST.getlist('fpath')


        #create folder hierarchy
        createfolders(pro,fpaths)
        
       
        for i,file in enumerate(files):
            if not checkstorage(pro,file.size):
                return HttpResponse(status=406)
            # Get the file name, __str__ property of the file object returned is the file name
            file_name = str(file)
            file_name = file_name.replace(' ','')
            foldername = fpaths[i].split('/')[-2]
            folder = Folder.objects.filter(owner=pro,name=foldername)[0]
            path = os.path.join(genesis,fpaths[i])
            uploadfinishedid = i
            with open(path, 'wb') as f:
                # Block writing large files to prevent stuck
                for chunk in file.chunks(chunk_size=2014):
                    f.write(chunk)
            if os.path.getsize(path):
                size = os.path.getsize(path)
            else:
                size = 0   
        
          

            dbfile = File.objects.create(owner=pro,name=file_name,path=path.replace(BASE_DIR,''),file_type=file_name.split('.')[-1].lower())
            dbfile.folder = folder
            dbfile.size = size
            folder.path = path.replace(dbfile.name, '')
            folder.folderfiles.add(dbfile)
            folder.save()
            dbfile.save()
            pro.storage += dbfile.size
            pro.save()   

            resp = fpaths[0].split('/')[0]
            
            resplist.append(resp)
            resplist.append('-')
            resplist.append(folder.id)
         

        return HttpResponse(resplist)




@csrf_exempt
def createsubfolders(pro,apath, pf):
    
    everyfilepath = apath
    ret = {}
    directories = []
    gpath = pf.path
    print('createsubfolders pf=',gpath)
    if everyfilepath:
        #separate every filepath into a list element 
       
       
        for pathindex, path in enumerate(everyfilepath):
            

            dirlist = path.split('/')
            fname = dirlist.pop()
            fullpath = gpath+path.replace(fname,'')
            if os.path.exists(fullpath):
                pass
            else:
                os.makedirs(fullpath)
            directories.append(dirlist)
        #remove duplicate folders to create database structure
        dirset = set()   
        for mydir in directories:
            dirset.add(tuple(mydir))

        dirlist = []
        for item in dirset:
            dirlist.append(list(item))

        g = pf
        for mdir in dirlist:
            parentf = None
            if len(mdir) == 1:
                if Folder.objects.filter(name=str(mdir[0]),owner=pro,parent=g).exists():
                    pass
                else:
                    f = Folder.objects.create(name=str(mdir[0]), parent=g,owner=pro)
                g.children.add(f)
                g.save()

            else:

                i = 0
                temp = None
                while i < len(mdir):
                    if i == 0:
                        if Folder.objects.filter(name=str(mdir[i]),owner=pro).exists():
                            temp = Folder.objects.filter(name=str(mdir[i]), owner=pro)[0]
                        else:
                            f = Folder.objects.create(name=str(mdir[i]), parent=g,owner=pro)
                            temp = f
                            g.children.add(f)
                            g.save()
                    else:
                        if Folder.objects.filter(name=str(mdir[i]), owner=pro).exists():
                            temp = Folder.objects.filter(name=str(mdir[i]), owner=pro)[0]
                        else:
                            f = Folder.objects.create(name=str(mdir[i]), parent=temp,owner=pro)
                            temp.children.add(f)
                            temp.save()
                            temp = f
                    i += 1 
    return 



@csrf_exempt
def sub_files_upload(request):
    parentfolder = Folder.objects.get(id=request.session['fid'])
    print('parentpath ',parentfolder.path)
    d = {}
    resplist = []
    pro = Profile.objects.get(user=request.user)
    genesis = getgenesis(pro)
    if request.method == 'GET':
        return render(request, 'uploads/my-drive.html',{})
    elif request.is_ajax(): 
        # The file object to take name attribute value input box
        files = request.FILES.getlist('files')
        fpaths = request.POST.getlist('fpath')


        #create folder hierarchy
        createsubfolders(pro,fpaths,parentfolder)
        
       
        for i,file in enumerate(files):
            if not checkstorage(pro,file.size):
                return HttpResponse(status=406)
            # Get the file name, __str__ property of the file object returned is the file name
            file_name = str(file)
            file_name = file_name.replace(' ','')
            foldername = fpaths[i].split('/')[-2]
            folder = Folder.objects.filter(owner=pro,name=foldername)[0]
            path = os.path.join(parentfolder.path,fpaths[i])
            uploadfinishedid = i
            with open(path, 'wb') as f:
                # Block writing large files to prevent stuck
                for chunk in file.chunks(chunk_size=2014):
                    f.write(chunk)
            if os.path.getsize(path):
                size = os.path.getsize(path)
            else:
                size = 0   
        
          

            dbfile = File.objects.create(owner=pro,name=file_name,path=path.replace(BASE_DIR,''),file_type=file_name.split('.')[-1].lower())
            dbfile.folder = folder
            dbfile.size = size
            folder.path = path.replace(dbfile.name, '')
            folder.folderfiles.add(dbfile)
            folder.save()
            dbfile.save()
            pro.storage += dbfile.size
            pro.save()   

            resp = fpaths[0].split('/')[0]
            
            resplist.append(resp)
            resplist.append('-')
            resplist.append(folder.id)
         

        return HttpResponse(resplist)
