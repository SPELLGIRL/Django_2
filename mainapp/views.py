from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpRequest
from .models import Product, Category, CatalogMenu, MainMenu, NewMenu, Address
from basketapp.models import Basket
from random import sample
import os

main_menu_links = MainMenu.objects.all()

content = {
    'main_menu_links': main_menu_links
}


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return None


def index(request: HttpRequest, current_product_category=''):
    new_menu_check = NewMenu.objects.filter(category__is_active=True)
    if current_product_category != '':
        get_object_or_404(NewMenu,
                          category__name=current_product_category,
                          pk__gt=1,
                          category__is_active=True)
        new_menu_products = list(Product.objects.filter(
            category__name=current_product_category, is_active=True))
    else:
        if new_menu_check:
            new_menu_products = list(Product.objects.filter(
                category__name=new_menu_check.first().category.name,
                is_active=True))
        else:
            new_menu_products = []

    if new_menu_check:
        new_menu_links = [{'title': new_menu_check.first().title,
                           'category__name': ''}] + list(
            new_menu_check.values('title', 'category__name')[1:])
    else:
        new_menu_links = []

    used_product_categories = ['trending', 'exclusive', 'promo', 'hot']

    inner_content = {
        'title': 'Main',
        'new_menu_links': new_menu_links,
        'current_product_category': current_product_category,
        'new_menu_products': new_menu_products,
        'basket': get_basket(request.user),
    }

    for category in used_product_categories:
        if Category.objects.filter(name=category, is_active=True).first():
            _temp = list(Product.objects.filter(category__name=category,
                                                is_active=True))
            if _temp:
                inner_content[category + '_products'] = sample(_temp,
                                                               len(_temp))

    inner_content = {**content, **inner_content}
    return render(request, 'mainapp/index.html', inner_content)


def products(request: HttpRequest, current_product_category='', page=1):
    if current_product_category != '':
        get_object_or_404(CatalogMenu,
                          category__name=current_product_category,
                          category__is_active=True)
        catalog_menu_products = list(Product.objects.filter(
            category__name=current_product_category, is_active=True).order_by(
            'price'))
    else:
        catalog_menu_products = list(
            Product.objects.filter(is_active=True))

    provider = Paginator(catalog_menu_products, 6)

    try:
        products_provider = provider.page(page)
    except PageNotAnInteger:
        products_provider = provider.page(1)
    except EmptyPage:
        products_provider = provider.page(provider.num_pages)

    catalog_menu_links = [{'title': 'all',
                           'category__name': ''}] + list(
        CatalogMenu.objects.filter(category__is_active=True).values('title',
                                                                    'category__name'))

    used_product_categories = ['exclusive', 'promo']

    inner_content = {
        'title': 'Catalog',
        'catalog_menu_links': catalog_menu_links,
        'current_product_category': current_product_category,
        'provider': products_provider,
        'basket': get_basket(request.user),
    }

    for category in used_product_categories:
        if Category.objects.filter(name=category, is_active=True).first():
            _temp = list(Product.objects.filter(category__name=category,
                                                is_active=True))
            if _temp:
                inner_content[category + '_products'] = sample(_temp,
                                                               len(_temp))

    inner_content = {**content, **inner_content}

    return render(request, 'mainapp/products.html', inner_content)


def details(request: HttpRequest, product_id=None, color=None, size=None):
    current_product = get_object_or_404(Product, pk=product_id, is_active=True)

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

    catalog_menu_links = [{'title': 'all',
                           'category__name': ''}] + list(
        CatalogMenu.objects.filter(category__is_active=True).values('title',
                                                                    'category__name'))
    same_products = list(
        Product.objects.exclude(pk=product_id).filter(is_active=True,
                                                      category__in=current_product.category.filter(
                                                          is_active=True)))
    inner_content = {
        'title': current_product.title,
        'catalog_menu_links': catalog_menu_links,
        'color': color,
        'current_product': current_product,
        'product_id': product_id,
        'img_link': image_link,
        'same_products': sample(same_products, len(same_products)),
        'product_desc': current_product.full_description,
        'product_price': current_product.price,
        'basket': get_basket(request.user),
    }
    inner_content = {**content, **inner_content}

    return render(request, 'mainapp/details.html', inner_content)


def contacts(request: HttpRequest):
    addresses = list(Address.objects.all())
    inner_content = {
        'addresses': addresses,
        'title': 'Contacts',
        'basket': get_basket(request.user),
    }
    inner_content = {**content, **inner_content}
    return render(request, 'mainapp/contacts.html', inner_content)
