from controllers import ListViews, CreateViews, UpdateViews, DeleteViews, \
    DetailViews
import ordersapp.views as ordersapp
from django.urls import path

app_name = "ordersapp"

urlpatterns = [
    path('', ListViews.OrderList.as_view(), name='orders_list'),
    path('forming/complete/<int:pk>/',
         ordersapp.order_forming_complete, name='order_forming_complete'),
    path('create/', CreateViews.OrderItemsCreate.as_view(),
         name='order_create'),
    path('read/<int:pk>/', DetailViews.OrderRead.as_view(),
         name='order_read'),
    path('update/<int:pk>/', UpdateViews.OrderItemsUpdate.as_view(),
         name='order_update'),
    path('delete/<int:pk>/', DeleteViews.OrderDelete.as_view(),
         name='order_delete'),
    path('product/<int:pk>/price/', ordersapp.get_product_price),
]
