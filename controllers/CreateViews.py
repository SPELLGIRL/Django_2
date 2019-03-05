from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory
from ordersapp.forms import OrderItemForm
from authapp.forms import RegisterForm

from authapp.models import CustomUser
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


class OrderItemsCreate(CreateView):
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
