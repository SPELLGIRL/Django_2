from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpRequest
from django.contrib import auth
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from .forms import LoginForm, RegisterForm, UpdateForm
from .models import CustomUser


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

    context = {
        'title': title,
        'login_form': login_form
    }
    return render(request, 'authapp/login.html', context)


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
            user = register_form.save()
            if send_verify_mail(user):
                print('сообщение подтверждения отправлено')
            else:
                print('ошибка отправки сообщения')
            return HttpResponseRedirect(reverse('auth:login'))

    else:
        register_form = RegisterForm()

    context = {
        'title': title,
        'registration_form': register_form
    }

    return render(request, 'authapp/register.html', context)


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

    context = {
        'title': title,
        'update_form': update_form,
    }

    return render(request, 'authapp/edit.html', context)


def send_verify_mail(user):
    verify_link = reverse('auth:verify',
                          args=[user.email, user.activation_key])

    title = f'Confirm registration {user.username}'

    message = f'Для подтверждения учетной записи {user.username} на портале \
{settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email],
                     fail_silently=False)


def verify(request: HttpRequest, email, activation_key):
    title = 'Verification'

    context = {
        'title': title,
    }

    try:
        user = CustomUser.objects.get(email=email)

        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user,
                       backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html', context)
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html', context)
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('home'))
