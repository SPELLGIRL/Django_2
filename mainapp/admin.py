from django.contrib import admin
from .models import Product, Category, MainMenu, CatalogMenu, NewMenu, Address

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(MainMenu)
admin.site.register(CatalogMenu)
admin.site.register(NewMenu)
admin.site.register(Address)
