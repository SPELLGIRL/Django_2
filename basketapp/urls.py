from django.urls import path

import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name='view'),
    path('change/<int:pk>/', basketapp.basket_change, name='change'),
    path('delete/<int:pk>/', basketapp.basket_delete, name='delete'),
    # path('add/<int:pk>/', basketapp.basket_add, name='add'),
    # path('remove/<int:pk>/', basketapp.basket_remove, name='remove'),
]
