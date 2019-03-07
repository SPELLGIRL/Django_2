from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect, get_object_or_404
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

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductDeleteView, self).dispatch(request, *args,
                                                       **kwargs)


class OrderDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')

    def test_func(self):
        check = self.request.user == get_object_or_404(Order, id=self.kwargs[
            'pk']).user or self.request.user.is_superuser

        return check

    def is_active(self):
        return get_object_or_404(Order, id=self.kwargs['pk']).is_active

    def dispatch(self, request, *args, **kwargs):
        if self.is_active():
            return super(OrderDelete, self).dispatch(request, *args,
                                                     **kwargs)
        else:
            return HttpResponseRedirect(reverse('home:index'))
