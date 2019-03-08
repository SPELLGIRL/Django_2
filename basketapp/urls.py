from django.urls import path

import basketapp.views as basketapp

from controllers import ListViews

app_name = 'basketapp'

urlpatterns = [

    # FBV
    # path('', basketapp.basket, name='view'),
    path('add/<int:pk>/', basketapp.basket_add, name='add'),
    path('remove/<int:pk>/', basketapp.basket_remove, name='remove'),
    path('delete/<int:pk>/', basketapp.basket_delete, name='delete'),

    # CBV
    path('', ListViews.BasketListView.as_view(), name='view'),
    path('<int:page>/', ListViews.BasketListView.as_view(), name='view_page'),
]
