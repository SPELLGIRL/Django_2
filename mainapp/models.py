from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Категория'
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MainMenu(models.Model):
    title = models.CharField(max_length=20, verbose_name='Заголовок')
    link = models.CharField(max_length=200, unique=True, verbose_name='Ссылка')

    def __str__(self):
        return self.title


class CatalogMenu(models.Model):
    title = models.CharField(max_length=20, verbose_name='Заголовок')
    category = models.OneToOneField(
        Category,
        on_delete=models.CASCADE,
        unique=True,
        verbose_name='Категория'
    )

    def __str__(self):
        return self.title


class NewMenu(models.Model):
    title = models.CharField(max_length=20, verbose_name='Заголовок')
    category = models.OneToOneField(
        Category,
        on_delete=models.CASCADE,
        unique=True,
        verbose_name='Категория'
    )

    def __str__(self):
        return self.title


class Address(models.Model):
    city = models.CharField(max_length=50, verbose_name='Город')
    phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='E-Mail')
    address = models.CharField(max_length=150, verbose_name='Адрес')

    def __str__(self):
        return f'{self.id} {self.city} {self.address}'


class Product(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True)
    small_img_path = models.ImageField(
        upload_to='product_small_img',
        verbose_name='Миниатюра',
        blank=True
    )
    big_img_path = models.ImageField(
        upload_to='product_big_img',
        verbose_name='Изображение',
        blank=True
    )

    category = models.ManyToManyField(
        Category,
        blank=True,
        verbose_name='Категория',
        related_name='products',
    )

    full_description = models.TextField(verbose_name='Подробное описание',
                                        blank=True)

    price = models.DecimalField(verbose_name='Цена',
                                default=0,
                                max_digits=8,
                                decimal_places=2)

    quantity = models.PositiveIntegerField(verbose_name='Количество на складе',
                                           default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
