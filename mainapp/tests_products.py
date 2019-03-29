from django.test import TestCase
from mainapp.models import Product, Category


class ProductsTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name="стулья")
        self.product_1 = Product.objects.create(title="стул 1",
                                                price=1999.5,
                                                quantity=150)
        self.product_1.category.add(category)

        self.product_2 = Product.objects.create(title="стул 2",
                                                price=2998.1,
                                                quantity=125,
                                                is_active=False)
        self.product_2.category.add(category)

        self.product_3 = Product.objects.create(title="стул 3",
                                                price=998.1,
                                                quantity=115)
        self.product_3.category.add(category)

    def test_product_get(self):
        product_1 = Product.objects.get(title="стул 1")
        product_2 = Product.objects.get(title="стул 2")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Product.objects.get(title="стул 1")
        product_2 = Product.objects.get(title="стул 2")
        self.assertEqual(str(product_1), 'стул 1')
        self.assertEqual(str(product_2), 'стул 2')

    def test_product_get_items(self):
        product_1 = Product.objects.get(title="стул 1")
        product_3 = Product.objects.get(title="стул 3")
        products = product_1.get_items()

        self.assertEqual(list(products), [product_1, product_3])
