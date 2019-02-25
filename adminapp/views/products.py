from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test
from mainapp.models import Category, Product
from adminapp.models.products import ProductEditForm


def get_product_categories(pk):
    product = Product.objects.get(pk=pk)
    return product.category.all()


@user_passes_test(lambda user: user.is_superuser)
def create(request: HttpRequest, pk):
    title = 'продукт/создание'
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    content = {
        'title': title,
        'update_form': product_form,
        'category': category
    }

    return render(request, 'adminapp/products/update.html', content)


@user_passes_test(lambda user: user.is_superuser)
def read(request: HttpRequest, id):
    title = 'Product'
    product = get_object_or_404(Product, pk=id)
    content = {
        'title': title,
        'object': product,
        'categories': get_product_categories(id)
    }

    return render(request, 'adminapp/products/read.html', content)


@user_passes_test(lambda user: user.is_superuser)
def list_by_category(request: HttpRequest, pk, page=1):
    title = 'админка/продукт'

    category = get_object_or_404(Category, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by(
        '-is_active')

    provider = Paginator(products_list, 5)

    try:
        products_provider = provider.page(page)
    except PageNotAnInteger:
        products_provider = provider.page(1)
    except EmptyPage:
        products_provider = provider.page(provider.num_pages)

    content = {
        'title': title,
        'category': category,
        'provider': products_provider,
    }

    return render(request, 'adminapp/products/index.html', content)


@user_passes_test(lambda user: user.is_superuser)
def update(request: HttpRequest, id):
    title = 'продукт/редактирование'

    edit_product = get_object_or_404(Product, pk=id)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES,
                                    instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(
                reverse('admin:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    content = {
        'title': title,
        'update_form': edit_form,
        'product': edit_product
    }

    return render(request, 'adminapp/products/update.html', content)


@user_passes_test(lambda user: user.is_superuser)
def delete(request: HttpRequest, id):
    title = 'продукт/удаление'

    product = get_object_or_404(Product, pk=id)

    categories = get_product_categories(id)

    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(
            reverse('admin:product_read', args=[product.pk]))

    content = {
        'title': title,
        'product_to_delete': product,
        'categories': categories
    }

    return render(request, 'adminapp/products/delete.html', content)
