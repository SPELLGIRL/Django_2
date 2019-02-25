from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpRequest
from django.contrib import auth
from django.urls import reverse

from .forms import LoginForm, RegisterForm, UpdateForm
from mainapp.models import MainMenu
from basketapp.models import Basket

main_menu_links = MainMenu.objects.all()

content = {
    'main_menu_links': main_menu_links
}


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def login(request: HttpRequest):
    title = 'Sign In'

    login_form = LoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST.get('next', '/')

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(next_url)

    inner_content = {
        'title': title,
        'login_form': login_form
    }
    inner_content = {**content, **inner_content}
    return render(request, 'authapp/login.html', inner_content)


def logout(request: HttpRequest):
    auth.logout(request)
    return HttpResponseRedirect('/')


def redirect_to_login(request: HttpRequest):
    return HttpResponseRedirect('/auth/login')


def register(request: HttpRequest):
    title = 'Registration'

    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))

    else:
        register_form = RegisterForm()

    inner_content = {
        'title': title,
        'registration_form': register_form
    }
    inner_content = {**content, **inner_content}

    return render(request, 'authapp/register.html', inner_content)


def edit(request: HttpRequest):
    title = 'Profile'

    if request.method == 'POST':
        update_form = UpdateForm(request.POST, request.FILES,
                                 instance=request.user)

        if update_form.is_valid():
            update_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))

    else:
        update_form = UpdateForm(instance=request.user)

    inner_content = {
        'title': title,
        'update_form': update_form,
        'basket': get_basket(request.user),
    }

    inner_content = {**content, **inner_content}

    return render(request, 'authapp/edit.html', inner_content)

