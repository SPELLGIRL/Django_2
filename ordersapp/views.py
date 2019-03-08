from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest

from ordersapp.models import Order


def order_forming_complete(request: HttpRequest, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('order:orders_list'))
