from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpRequest
from .models import Product, Category, CatalogMenu, NewMenu, Address
from random import sample
import os
from django.conf import settings
from django.core.cache import cache


def index(request: HttpRequest, current_product_category=''):
    if current_product_category != '':
        get_object_or_404(NewMenu,
                          category__name=current_product_category,
                          pk__gt=1,
                          category__is_active=True)
        new_menu_products = get_products_by_category_random(
            current_product_category)
    else:
        if get_new_menu_check_cached():
            new_menu_products = get_products_by_category_random(
                get_new_menu_check()[0]['category__name'])
        else:
            new_menu_products = []

    new_menu_links = get_new_menu_links_cached()

    used_product_categories = ['trending', 'exclusive', 'promo', 'hot']

    context = {
        'title': 'Main',
        'new_menu_links': new_menu_links,
        'current_product_category': current_product_category,
        'new_menu_products': new_menu_products,
    }

    for category in used_product_categories:
        if Category.objects.filter(name=category, is_active=True).values(
                'id').first():
            if get_products_by_category_random(category):
                context[
                    category + '_products'] = get_products_by_category_random(
                    category)

    return render(request, 'mainapp/index.html', context)


def products(request: HttpRequest, current_product_category='', page=1):
    if current_product_category != '':
        get_object_or_404(CatalogMenu,
                          category__name=current_product_category,
                          category__is_active=True)
        catalog_menu_products = get_products_by_category_random(
            current_product_category)
    else:
        catalog_menu_products = get_products_by_category_random('')

    provider = Paginator(catalog_menu_products, 6)

    try:
        products_provider = provider.page(page)
    except PageNotAnInteger:
        products_provider = provider.page(1)
    except EmptyPage:
        products_provider = provider.page(provider.num_pages)

    catalog_menu_links = get_catalog_menu_links_cached()

    used_product_categories = ['exclusive', 'promo']

    context = {
        'title': 'Catalog',
        'catalog_menu_links': catalog_menu_links,
        'current_product_category': current_product_category,
        'provider': products_provider,
    }

    for category in used_product_categories:
        if Category.objects.filter(name=category, is_active=True).first():
            _temp = list(Product.objects.filter(category__name=category,
                                                is_active=True))
            if _temp:
                context[category + '_products'] = sample(_temp,
                                                         len(_temp))

    return render(request, 'mainapp/products.html', context)


def details(request: HttpRequest, product_id=None, color=None, size=None):
    current_product = get_product(product_id)

    if current_product.big_img_path and size is None:
        image_link = current_product.big_img_path.url
        if color:
            split = os.path.split(image_link)
            check_color = split[0] + str(color) + split[1]
            image_link = check_color if os.path.exists(
                check_color) else current_product.big_img_path.url
    elif current_product.small_img_path:
        image_link = current_product.small_img_path.url
    else:
        image_link = ''

    catalog_menu_links = get_catalog_menu_links()

    same_products = list(
        Product.objects.exclude(pk=product_id).filter(is_active=True,
                                                      category__in=current_product.category.filter(
                                                          is_active=True)))
    context = {
        'title': current_product.title,
        'catalog_menu_links': catalog_menu_links,
        'color': color,
        'current_product': current_product,
        'product_id': product_id,
        'img_link': image_link,
        'same_products': sample(same_products, len(same_products)),
        'product_desc': current_product.full_description,
        'product_price': current_product.price,
    }

    return render(request, 'mainapp/details.html', context)


def contacts(request: HttpRequest):
    addresses = list(Address.objects.all())
    context = {
        'addresses': addresses,
        'title': 'Contacts',
    }
    return render(request, 'mainapp/contacts.html', context)


def get_catalog_menu_links():
    catalog_menu_links = [{'title': 'all',
                           'category__name': ''}] + list(
        CatalogMenu.objects.select_related('category').filter(
            category__is_active=True).values(
            'title',
            'category__name'))

    return catalog_menu_links


def get_catalog_menu_links_cached():
    if settings.LOW_CACHE:
        key = 'catalog_menu_links_cached'
        catalog_menu_links_cached = cache.get(key)
        if catalog_menu_links_cached is None:
            catalog_menu_links_cached = get_catalog_menu_links()
            cache.set(key, catalog_menu_links_cached)
        return catalog_menu_links_cached
    else:
        return get_catalog_menu_links()


def get_new_menu_check():
    return NewMenu.objects.select_related('category').filter(
        category__is_active=True).values('title', 'category_id',
                                         'category__name')


def get_new_menu_check_cached():
    if settings.LOW_CACHE:
        key = 'new_menu_check_cached'
        new_menu_check_cached = cache.get(key)
        if new_menu_check_cached is None:
            new_menu_check_cached = get_new_menu_check()
        return new_menu_check_cached
    else:
        return get_new_menu_check()


def get_new_menu_links():
    if get_new_menu_check_cached():
        new_menu_links = [{'title': get_new_menu_check_cached()[0]['title'],
                           'category__name': ''}] + list(
            get_new_menu_check_cached().values('title', 'category__name')[1:])
    else:
        new_menu_links = []

    return new_menu_links


def get_new_menu_links_cached():
    if settings.LOW_CACHE:
        key = 'new_menu_links_cached'
        new_menu_links_cached = cache.get(key)
        if new_menu_links_cached is None:
            new_menu_links_cached = get_new_menu_links()
            cache.set(key, new_menu_links_cached)
        return new_menu_links_cached
    else:
        return get_new_menu_links()


def get_products_by_category_price(category):
    if category == '':
        products_price = Product.objects.filter(is_active=True).order_by(
            'price')
    else:
        products_price = Product.objects.prefetch_related('category').filter(
            category__name=category, is_active=True).order_by('price')
    return products_price


def get_products_by_category_price_cached(category):
    if settings.LOW_CACHE:
        key = f'products_by_category_price_cached{category}'
        products_by_category_price_cached = cache.get(key)
        if products_by_category_price_cached is None:
            products_by_category_price_cached = get_products_by_category_price(
                category)
            cache.set(key, products_by_category_price_cached)
        return products_by_category_price_cached
    else:
        return get_products_by_category_price(category)


def get_products_by_category_random(category):
    _temp = list(get_products_by_category_price_cached(category))
    return sample(_temp, len(_temp))


def get_product(product_id):
    if settings.LOW_CACHE:
        key = f'product_{product_id}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=product_id, is_active=True)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=product_id, is_active=True)
