from django.urls import path

import mainapp.views as controller

app_name = 'mainapp'

urlpatterns = [
    path('', controller.products, name='index'),
    path('<int:page>/', controller.products, name='index_page'),
    path('details/<int:product_id>/', controller.details, name='product'),
    path('details/<int:product_id>/<str:color>/', controller.details,
         name='color'),
    path('<str:current_product_category>/',
         controller.products, name='category'),
    path('<str:current_product_category>/<int:page>/',
         controller.products, name='category_page')
]
