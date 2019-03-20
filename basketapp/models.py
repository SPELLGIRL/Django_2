from django.db import models
from django.conf import settings
from django.utils.functional import cached_property

from mainapp.models import Product


# class BasketQuerySet(models.QuerySet):
#
#     def delete(self, *args, **kwargs):
#         for item in self:
#             item.product.quantity += item.quantity
#             item.product.save()
#         super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество',
                                           default=0)
    add_datetime = models.DateTimeField(verbose_name='время',
                                        auto_now_add=True)

    def get_items(user):
        return Basket.objects.filter(user=user).order_by(
            'product__category')

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related().order_by(
            'product__category')

    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    @property
    def cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, _items)))

        # products = Basket.objects.filter(user=self.user)
        # total = sum([x.quantity for x in products])
        # return total

    @property
    def total_cost(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.cost, _items)))

        # products = Basket.objects.filter(user=self.user)
        # cost = sum([x.cost for x in products])
        # return cost

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - self.__class__.get_items(
    #             self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super(self.__class__, self).save(*args, **kwargs)
    #
    # def delete(self, *args, **kwargs):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(self.__class__, self).delete()
