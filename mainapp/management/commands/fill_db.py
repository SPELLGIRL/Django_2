from django.core.management.base import BaseCommand
from authapp.models import CustomUser

import json
import os

from django.db import connection

from mainapp.models import Product, Category, MainMenu, CatalogMenu, NewMenu, \
    Address

JSON_PATH = 'mainapp/load_data'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):

        clear = input('Clear databases in mainapp (y/n)? ').lower()
        if clear == 'y':
            CatalogMenu.objects.all().delete()
            MainMenu.objects.all().delete()
            NewMenu.objects.all().delete()
            Product.objects.all().delete()
            Address.objects.all().delete()
            Category.objects.all().delete()
            for i in (
                    'UPDATE SQLITE_SEQUENCE SET SEQ= 0 WHERE NAME="mainapp_category";',
                    'UPDATE SQLITE_SEQUENCE SET SEQ= 0 WHERE NAME="mainapp_product";',
                    'UPDATE SQLITE_SEQUENCE SET SEQ= 0 WHERE NAME="mainapp_mainmenu";',
                    'UPDATE SQLITE_SEQUENCE SET SEQ= 0 WHERE NAME="mainapp_catalogmenu";',
                    'UPDATE SQLITE_SEQUENCE SET SEQ= 0 WHERE NAME="mainapp_newmenu";',
                    'UPDATE SQLITE_SEQUENCE SET SEQ= 0 WHERE NAME="mainapp_address";',
                    'UPDATE SQLITE_SEQUENCE SET SEQ= 0 WHERE NAME="mainapp_product_category";'
            ):
                connection.cursor().execute(i)

        su = input('Create superuser (y/n)? ').lower()
        if su == 'y':
            CustomUser.objects.create_superuser(
                input('Введите имя суперпользователя: '),
                'django@geekmarket.local',
                input('Введите пароль суперпользователя: '),
                age=18
            )

        categories = load_from_json('all_categories')
        for category in categories:
            new_category = Category(**category)
            new_category.save()

        products = load_from_json('all_products')
        for product_data in products:
            category_names = product_data['category']
            product_data.pop('category')
            new_product = Product.objects.create(**product_data)
            for category_name in category_names:
                _category = Category.objects.get(name=category_name)
                new_product.category.add(_category)

        main_menu = load_from_json('main_menu')
        for link in main_menu:
            new_link = MainMenu(**link)
            new_link.save()

        new_menu = load_from_json('new_menu')
        for link in new_menu:
            category = Category.objects.get(name=link['category'])
            link['category'] = category
            new_link = NewMenu(**link)
            new_link.save()

        catalog_menu = load_from_json('catalog_menu')
        for link in catalog_menu:
            category = Category.objects.get(name=link['category'])
            link['category'] = category
            new_link = CatalogMenu(**link)
            new_link.save()

        addresses = load_from_json('all_addresses')
        for link in addresses:
            new_address = Address(**link)
            new_address.save()
