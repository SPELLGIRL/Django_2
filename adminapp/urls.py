from django.urls import path

from adminapp.views import users, categories, products
from controllers import ListViews, CreateViews, UpdateViews, DeleteViews, \
    DetailViews

app_name = 'adminapp'

urlpatterns = [
    # users

    # FBV
    # path('users/index/', users.index, name='users'),
    # path('users/index/<int:page>', users.index, name='users_page'),
    # path('users/create/', users.create, name='user_create'),
    # path('users/read/<int:pk>', users.read, name='user_read'),
    # path('users/update/<int:id>', users.update, name='user_update'),
    # path('users/delete/<int:pk>/', users.delete, name='user_delete'),

    # CBV
    path('users/index/', ListViews.UserListView.as_view(), name='users'),
    path('users/index/<int:page>/', ListViews.UserListView.as_view(),
         name='users_page'),
    path('users/create/', CreateViews.UserCreateView.as_view(),
         name='user_create'),
    path('users/read/<int:pk>/', DetailViews.UserDetailView.as_view(),
         name='user_read'),
    path('users/update/<int:pk>/', UpdateViews.UserUpdateView.as_view(),
         name='user_update'),
    path('users/delete/<int:pk>/', DeleteViews.UserDeleteView.as_view(),
         name='user_delete'),

    # categories

    # FBV
    # path('categories/index/', categories.index, name='categories'),
    # path('categories/create/', categories.create, name='category_create'),
    # path('categories/read/<int:pk>/', categories.read, name='category_read'),
    # path('categories/update/<int:pk>/', categories.update,
    #      name='category_update'),
    # path('categories/delete/<int:pk>/', categories.delete,
    #      name='category_delete'),

    # CBV
    path('categories/index/', ListViews.CategoryListView.as_view(),
         name='categories'),
    path('categories/index/<int:page>/', ListViews.CategoryListView.as_view(),
         name='categories_page'),
    path('categories/create/', CreateViews.CategoryCreateView.as_view(),
         name='category_create'),
    path('categories/read/<int:pk>/', DetailViews.CategoryDetailView.as_view(),
         name='category_read'),
    path('categories/update/<int:pk>/',
         UpdateViews.CategoryUpdateView.as_view(),
         name='category_update'),
    path('categories/delete/<int:pk>/',
         DeleteViews.CategoryDeleteView.as_view(),
         name='category_delete'),

    # products

    # FBV
    # path('products/list/<int:pk>/', products.list_by_category,
    #      name='products'),
    # path('products/list/<int:pk>/<int:page>/', products.list_by_category,
    #      name='products_page'),
    # path('products/create/<int:pk>/', products.create, name='product_create'),
    # path('products/read/<int:pk>/', products.read, name='product_read'),
    # path('products/update/<int:pk>/', products.update, name='product_update'),
    # path('products/delete/<int:pk>/', products.delete, name='product_delete'),

    # CBV
    path('products/list/<int:pk>/', ListViews.ProductListView.as_view(),
         name='products'),
    path('products/list/<int:pk>/<int:page>/',
         ListViews.ProductListView.as_view(),
         name='products_page'),
    path('products/create/<int:pk>/', CreateViews.ProductCreateView.as_view(),
         name='product_create'),
    path('products/read/<int:pk>/', DetailViews.ProductDetailView.as_view(),
         name='product_read'),
    path('products/update/<int:pk>/', UpdateViews.ProductUpdateView.as_view(),
         name='product_update'),
    path('products/delete/<int:pk>/', DeleteViews.ProductDeleteView.as_view(),
         name='product_delete'),
]
