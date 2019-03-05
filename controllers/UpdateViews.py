from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory
from ordersapp.forms import OrderItemForm

from authapp.models import CustomUser
from adminapp.models.users import UserEditForm
from ordersapp.models import Order, OrderItem


class UserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'adminapp/users/update.html'
    success_url = reverse_lazy('admin:users')
    form_class = UserEditForm

    def get_context_data(self, **kwargs):
        parent_context = super(UserUpdateView, self).get_context_data(**kwargs)
        parent_context['title'] = 'Update user'

        return parent_context

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

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
