from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from .forms import RegistrationForm
from django.shortcuts import render
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .signals import user_logged_in
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from .forms import UserLoginForm,CustomUserChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from uploads.views import getcontext
from django.apps import apps
from uploads.models import Profile

User = get_user_model()

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'core/createaccount.html'




def indexView(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        data = request.POST.copy()
        email = data.get('email')
        newu = User.objects.filter(email=email)
        if(newu):
          form = RegistrationForm()
          warningmsg = email + ' is already taken'
          context = {"alert":1,"warningmsg":warningmsg, 'form':form}
          return render(request, 'core/register-mountain.html', context)
        if form.is_valid():
              CustomUser = form.save()
            # Do something with the user
              messages.success(request, 'User saved successfully.')
              success_url = reverse_lazy('login')

        else:
            messages.error(request, 'The form is invalid.')

        return render(request, 'core/login.html', {'form': form})

    else:
        form = RegistrationForm()
        return render(request, 'core/register-mountain.html', {'form': form})


def validate_username(request):
    username = request.GET.get('username', None)

    #result checks if the username has an account
    result = User.objects.filter(email__contains=username).exists() | User.objects.filter(email__exact=username).exists()

    if(result):
            user = User.objects.filter(email__contains=username)[0]
            request.session['userid'] = user.id
    data = {
        'is_taken': result
    }
    return JsonResponse(data)

@csrf_exempt
def user_login(request):
    context = RequestContext(request)
    authentication_form = UserLoginForm
    form = UserLoginForm
    try:
      uid = request.session['userid']
    except KeyError:
      return render(None,'core/login.html', {'form':form})
    user = User.objects.get(id=uid)
    username = user.firstname
    initial = user.firstname[0]
    initial = initial.upper()
    if request.method == 'POST':
          username = str(user)
          password = request.POST['password']
          user = authenticate(username=username, password=password)
          if user is not None:
              if user.is_active:
                  login(request, user)
                  user_logged_in.send(user.__class__,instance=user,request=request)
                  # Redirect to index page.
                  return HttpResponseRedirect("/users/")
              else:
                  # Return a 'disabled account' error message
                  return HttpResponse("Your account is disabled.")
          else:
              # Return an 'invalid login' error message.
              return render(None,'core/login.html', {'form':form})
    else:
        # the login is a  GET request, so just show the user the login form.
        return render(None,'core/loginpw.html', {'form':form, 'user':user, 'initial':initial,'username':username})





def handler404(request, *args, **argv):
    response = render('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, 'core/500.html', {})

    response.status_code = 500
    return response


login_required(login_url='/users/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return render(request, 'core/change_password.html', {
            'form': form,
            'successalert':1,
            'successmsg':'password updated'
            })
        else:
             return render(request, 'core/change_password.html', {
            'form': form,
            'alert':1,
            'warningmsg':'invalid password or passwords do not match'
            })
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'core/change_password.html', {
        'form': form
    })


login_required(login_url='/users/login/')
def change_email(request):
  p = apps.get_model('profiles.Profile')
  context = getcontext(request)
  if request.method == 'POST':
    qemail = request.POST.get('qemail', None)
    if qemail == '':
      context.update({"alert":1,"warningmsg":"must enter data"})
      return render(request, 'core/change_email.html',context)
    elif '@' not in qemail:
      context.update({"alert":1,"warningmsg":"must enter a valid email"})
      return render(request, 'core/change_email.html',context)

    request.user.email = qemail
    request.user.save()
  else:
    return render(request, 'core/change_email.html',context)
  context.update({"successalert":1,"successmsg":"Email updated"})
  return render(request, 'core/change_email.html',context)

login_required(login_url='/users/login/')
def changename(request):
    if request.method == 'POST':
        qfirstname = request.POST.get('qfirstname', None)
        qlastname = request.POST.get('qlastname', None)
        if qfirstname == '' and qlastname == '':
          return render(request, 'core/changename.html',{"alert":1,"warningmsg":"must enter data"})
        elif qfirstname == '':
          return render(request, 'core/changename.html',{"alert":1,"warningmsg":"must enter a firstname"})
        elif qlastname == '':
          return render(request, 'core/changename.html',{"alert":1,"warningmsg":"must enter a lastname"})
      
        request.user.firstname = qfirstname
        request.user.lastname = qlastname
        request.user.save()

    else:
        return render(request, 'core/changename.html')
    return render(request, 'core/changename.html',{"successalert":1,"successmsg":"Names updated"})




login_required(login_url='/users/login/')
def changenumber(request):
  context = getcontext(request)
  if request.method == 'POST':
    qnumber = request.POST.get('qnumber', None)
    if qnumber == '':
      context.update({"alert":1,"warningmsg":"must enter data"})
      return render(request, 'core/changenumber.html',context)

    p = Profile.objects.get(user=request.user)
    p.number = str(qnumber)
    p.save()
                   
    
  else:
    return render(request, 'core/changenumber.html',context)
  context.update({"successalert":1,"successmsg":"Number updated"})
  return render(request, 'core/changenumber.html',context)



login_required(login_url='/users/login/')
def accountview(request):
    context = getcontext(request)
    return render(request, 'core/account.html',context)
