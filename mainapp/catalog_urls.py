from django.urls import path
from django.views.decorators.cache import cache_page

import mainapp.views as controller

app_name = 'mainapp'

urlpatterns = [
    path('', controller.products, name='index'),
    path('ajax/', cache_page(3600)(controller.products_ajax)),
    path('<int:page>/', controller.products, name='index_page'),
    path('<int:page>/ajax/', cache_page(3600)(controller.products_ajax)),
    path('details/<int:product_id>/', controller.details, name='product'),
    path('details/<int:product_id>/<str:color>/', controller.details,
         name='color'),
    path('<str:current_product_category>/',
         controller.products, name='category'),
    path('<str:current_product_category>/ajax/',
         cache_page(3600)(controller.products_ajax)),
    path('<str:current_product_category>/<int:page>/',
         controller.products, name='category_page'),
    path('<str:current_product_category>/<int:page>/ajax/',
         cache_page(3600)(controller.products_ajax)),
]
