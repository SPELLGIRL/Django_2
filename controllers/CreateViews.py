from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory
from ordersapp.forms import OrderItemForm
from authapp.forms import RegisterForm
from adminapp.models.categories import CategoryEditForm
from adminapp.models.products import ProductEditForm

from authapp.models import CustomUser
from mainapp.models import Category, Product
from ordersapp.models import Order, OrderItem
from basketapp.models import Basket


class UserCreateView(CreateView):
    model = CustomUser
    template_name = 'adminapp/users/update.html'
    success_url = reverse_lazy('admin:users')
    form_class = RegisterForm

    def get_context_data(self, **kwargs):
        parent_context = super(UserCreateView, self).get_context_data(**kwargs)
        parent_context['title'] = 'Create user'

        return parent_context

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'adminapp/categories/update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = CategoryEditForm

    def get_context_data(self, **kwargs):
        parent_context = super(CategoryCreateView, self).get_context_data(
            **kwargs)
        parent_context['title'] = 'Create category'

        return parent_context

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryCreateView, self).dispatch(request, *args,
                                                        **kwargs)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/products/update.html'
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse('admin:products', args=[self.kwargs['pk']])

    def get_context_data(self, **kwargs):
        parent_context = super(ProductCreateView, self).get_context_data(
            **kwargs)
        parent_context['title'] = 'Create product'
        parent_context['category'] = get_object_or_404(Category,
                                                       pk=self.kwargs['pk'])

        return parent_context

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductCreateView, self).dispatch(request, *args,
                                                       **kwargs)


class OrderItemsCreate(LoginRequiredMixin, CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        orderformset = inlineformset_factory(Order, OrderItem,
                                             form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = orderformset(self.request.POST)
        else:
            basket_items = Basket.get_items(self.request.user)
            if len(basket_items):
                data['basket_items'] = basket_items
                orderformset = inlineformset_factory(Order, OrderItem,
                                                     form=OrderItemForm,
                                                     extra=len(basket_items))
                formset = orderformset()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
            else:
                formset = orderformset()

        data['orderitems'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']
        basket_items = Basket.get_items(self.request.user)

        with transaction.atomic():
            basket_items.delete()
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # if self.object.get_total_cost() == 0:
        #     self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)
