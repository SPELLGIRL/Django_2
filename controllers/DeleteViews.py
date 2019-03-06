from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from authapp.models import CustomUser
from mainapp.models import Category, Product
from ordersapp.models import Order


class UserDeleteView(DeleteView):
    model = CustomUser
    template_name = 'adminapp/users/delete.html'
    success_url = reverse_lazy('admin:users')

    def get_context_data(self, **kwargs):
        parent_context = super(UserDeleteView, self).get_context_data(**kwargs)
        parent_context['title'] = 'Delete user'

        return parent_context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'adminapp/categories/delete.html'
    success_url = reverse_lazy('admin:categories')

    def get_context_data(self, **kwargs):
        parent_context = super(CategoryDeleteView, self).get_context_data(
            **kwargs)
        parent_context['title'] = 'Delete category'

        return parent_context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryDeleteView, self).dispatch(request, *args,
                                                        **kwargs)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/products/delete.html'

    def get_success_url(self):
        return reverse('admin:product_read', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        parent_context = super(ProductDeleteView, self).get_context_data(
            **kwargs)
        parent_context['title'] = 'Delete product'
        parent_context['categories'] = self.object.category.all()

        return parent_context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductDeleteView, self).dispatch(request, *args,
                                                       **kwargs)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        order.is_active = False
        order.save()
        return HttpResponseRedirect(self.success_url)
