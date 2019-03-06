from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from authapp.models import CustomUser
from mainapp.models import Category, Product
from ordersapp.models import Order


class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'adminapp/users/read.html'

    def get_context_data(self, **kwargs):
        parent_context = super(UserDetailView, self).get_context_data(**kwargs)
        parent_context['title'] = 'User view'

        return parent_context

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDetailView, self).dispatch(request, *args, **kwargs)


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'adminapp/categories/read.html'

    def get_context_data(self, **kwargs):
        parent_context = super(CategoryDetailView, self).get_context_data(
            **kwargs)
        parent_context['title'] = 'User view'
        parent_context['products'] = self.object.products.all().order_by(
            'is_active')[:5]

        return parent_context

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryDetailView, self).dispatch(request, *args,
                                                        **kwargs)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/products/read.html'

    def get_context_data(self, **kwargs):
        parent_context = super(ProductDetailView, self).get_context_data(
            **kwargs)
        parent_context['title'] = 'User view'
        parent_context['categories'] = self.object.category.all()

        return parent_context

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductDetailView, self).dispatch(request, *args,
                                                       **kwargs)


class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context
