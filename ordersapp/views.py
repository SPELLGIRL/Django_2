from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, JsonResponse
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

from ordersapp.models import Order, OrderItem
from basketapp.models import Basket
from mainapp.models import Product


def order_forming_complete(request: HttpRequest, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('order:orders_list'))


def get_product_price(request, pk):
    if request.is_ajax():
        product = get_object_or_404(Product, pk=int(pk))
        if product:
            return JsonResponse({'price': product.price})
        else:
            return JsonResponse({'price': 0})


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if update_fields is 'quantity' or 'product':
        if instance.pk:
            instance.product.quantity -= instance.quantity - \
                                         sender.get_item(instance.pk).quantity
        else:
            instance.product.quantity -= instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
