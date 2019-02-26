from django.urls import path

import authapp.views as controller

app_name = 'authapp'

urlpatterns = [
    path('', controller.redirect_to_login, name='index'),
    path('login/', controller.login, name='login'),
    path('logout/', controller.logout, name='logout'),
    path('register/', controller.register, name='register'),
    path('edit/', controller.edit, name='edit'),
    path('verify//<str:email>)/<str:activation_key>)/',
         controller.send_verify_mail, name='verify'),
]
