from django.urls import path

from adminapp.views import users, categories, products
from controllers import ListViews, CreateViews, UpdateViews, DeleteViews, \
    DetailViews

app_name = 'adminapp'

urlpatterns = [
    # users
    path('users/index/', ListViews.UserListView.as_view(), name='users'),
    # path('users/index/', users.index, name='users'),
    path('users/index/<int:page>/', ListViews.UserListView.as_view(),
         name='users_page'),
    # path('users/index/<int:page>', users.index, name='users_page'),
    path('users/create/', CreateViews.UserCreateView.as_view(),
         name='user_create'),
    # path('users/create/', users.create, name='user_create'),
    path('users/read/<int:pk>/', DetailViews.UserDetailView.as_view(),
         name='user_read'),
    # path('users/read/<int:pk>', users.read, name='user_read'),
    path('users/update/<int:pk>/', UpdateViews.UserUpdateView.as_view(),
         name='user_update'),
    # path('users/update/<int:id>', users.update, name='user_update'),
    path('users/delete/<int:pk>/', DeleteViews.UserDeleteView.as_view(),
         name='user_delete'),

    # categories
    path('categories/index/', categories.index, name='categories'),
    path('categories/create/', categories.create, name='category_create'),
    path('categories/read/<int:id>/', categories.read, name='category_read'),
    path('categories/update/<int:id>/', categories.update,
         name='category_update'),
    path('categories/delete/<int:id>/', categories.delete,
         name='category_delete'),

    # products
    path('products/create/<int:pk>/', products.create, name='product_create'),
    path('products/read/<int:id>/', products.read, name='product_read'),
    path('products/list/<int:pk>/', products.list_by_category,
         name='products'),
    path('products/list/<int:pk>/<int:page>/', products.list_by_category,
         name='products_page'),
    path('products/update/<int:id>/', products.update, name='product_update'),
    path('products/delete/<int:id>/', products.delete, name='product_delete'),
]
