from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory
from ordersapp.forms import OrderItemForm

from authapp.models import CustomUser
from mainapp.models import Category, Product
from adminapp.models.users import UserEditForm
from adminapp.models.categories import CategoryEditForm
from adminapp.models.products import ProductEditForm
from ordersapp.models import Order, OrderItem


class UserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'adminapp/users/update.html'
    success_url = reverse_lazy('admin:users')
    form_class = UserEditForm

    def get_context_data(self, **kwargs):
        parent_context = super(UserUpdateView, self).get_context_data(**kwargs)
        parent_context['title'] = 'Edit user'

        return parent_context

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'adminapp/categories/update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = CategoryEditForm

    def get_context_data(self, **kwargs):
        parent_context = super(CategoryUpdateView, self).get_context_data(
            **kwargs)
        parent_context['title'] = 'Edit category'

        return parent_context

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryUpdateView, self).dispatch(request, *args,
                                                        **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/products/update.html'
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse('admin:product_update', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        parent_context = super(ProductUpdateView, self).get_context_data(
            **kwargs)
        parent_context['title'] = 'Edit product'

        return parent_context

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductUpdateView, self).dispatch(request, *args,
                                                       **kwargs)


class OrderItemsUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    def test_func(self):
        check = self.request.user == get_object_or_404(Order, id=self.kwargs[
            'pk']).user or self.request.user.is_superuser

        return check

    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        orderformset = inlineformset_factory(Order,
                                             OrderItem,
                                             form=OrderItemForm,
                                             extra=1)
        if self.request.POST:
            data['orderitems'] = orderformset(self.request.POST,
                                              instance=self.object)
        else:
            data['orderitems'] = orderformset(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        return super(OrderItemsUpdate, self).form_valid(form)
