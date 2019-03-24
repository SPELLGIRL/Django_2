from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.decorators import user_passes_test
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection

from mainapp.models import Category
from adminapp.models.categories import CategoryEditForm


@user_passes_test(lambda user: user.is_superuser)
def index(request: HttpRequest):
    models = Category.objects.all()

    context = {
        'title': 'Categories list',
        'models': models,
    }

    return render(request, 'adminapp/categories/index.html', context)


@user_passes_test(lambda user: user.is_superuser)
def create(request: HttpRequest):
    if request.method == 'POST':
        form = CategoryEditForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        form = CategoryEditForm()

    context = {
        'title': 'Category create',
        'form': form,
    }

    return render(request, 'adminapp/categories/update.html', context)


@user_passes_test(lambda user: user.is_superuser)
def read(request: HttpRequest, pk):
    model = get_object_or_404(Category, pk=pk)
    context = {
        'title': 'Category',
        'object': model,
        'products': model.products.all().order_by('is_active')[:5],
    }

    return render(request, 'adminapp/categories/read.html', context)


@user_passes_test(lambda user: user.is_superuser)
def update(request: HttpRequest, pk):
    model = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryEditForm(request.POST, request.FILES, instance=model)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('adminapp:category_read', args=[model.pk]))
    else:
        form = CategoryEditForm(instance=model)

    context = {
        'title': 'Category update',
        'form': form,
        'object': model,
    }

    return render(request, 'adminapp/categories/update.html', context)


@user_passes_test(lambda user: user.is_superuser)
def delete(request: HttpRequest, pk):
    model = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        model.is_active = False
        model.save()
        return HttpResponseRedirect(reverse('admin:categories'))

    context = {
        'title': 'Category delete',
        'object': model,
    }

    return render(request, 'adminapp/categories/delete.html', context)


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=Category)
def product_is_active_update_category_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.products.all().update(is_active=True)
        else:
            instance.products.all().update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
