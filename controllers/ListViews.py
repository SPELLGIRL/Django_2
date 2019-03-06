from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404

from authapp.models import CustomUser
from mainapp.models import Category, Product
from ordersapp.models import Order


class UserListView(ListView):
    model = CustomUser
    template_name = 'adminapp/users/index.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        parent_context = super(UserListView, self).get_context_data(**kwargs)
        parent_context['title'] = 'Users list'

        return parent_context

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)


class CategoryListView(ListView):
    model = Category
    template_name = 'adminapp/categories/index.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        parent_context = super(CategoryListView, self).get_context_data(
            **kwargs)
        parent_context['title'] = 'Category list'

        return parent_context

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryListView, self).dispatch(request, *args, **kwargs)


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products/index.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        parent_context = super(ProductListView, self).get_context_data(
            **kwargs)
        parent_context['title'] = 'Product by category'
        parent_context['category'] = get_object_or_404(Category,
                                                       pk=self.kwargs['pk'])

        return parent_context

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs['pk']).order_by(
            '-is_active')

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductListView, self).dispatch(request, *args, **kwargs)


class OrderList(LoginRequiredMixin, ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
