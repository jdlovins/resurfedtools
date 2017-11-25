from django.core.exceptions import PermissionDenied
from django.forms import Textarea
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.forms.models import inlineformset_factory
from .forms import SignUpForm, LoginForm, UserForm  #, ProfileForm
from .decorators import custom_login_required
from .models import User
# Create your views here.

from time import sleep

def index(request):
    if request.user.is_authenticated():
        pass

    next_url = request.GET.get('next')

    sleep(5)

    signup_form = SignUpForm()
    login_form = LoginForm()
    return render(request, 'index.html', {'signup_form': signup_form, 'login_form': login_form, 'next': next_url})


def login_user(request):
    if request.user.is_authenticated():
        redirect(index)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            user_name = form.cleaned_data.get('user_name')
            password = form.cleaned_data.get('password')

            user = authenticate(username=user_name, password=password)

            if user is not None:
                if not request.POST.get('remember_me', None):
                    request.session.set_expiry(0)
                login(request, user)
            else:
                messages.error(request, "Username or Password is invalid, please try again.")

        else:
            messages.error(request, form.errors)

    next_url = request.POST.get('next')

    if next_url is not None:
        return redirect(next_url)
    else:
        return redirect(index)


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            user_name = form.cleaned_data.get('user_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = User.objects.create_user(user_name, email, password)
            user.save()
            login(request, user)

            return redirect(index)
        else:
            #for e in form.errors:
                #for ee in form[e].errors:
                messages.error(request, form.errors)

    return redirect(index)


def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect(index)


@custom_login_required
def user_profile(request):
    pass
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect(user_profile)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
    return render(request, 'account/profile.html', {
        'user_form': user_form
    })
