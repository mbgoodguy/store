from django.db import models
from django.urls import reverse

from users.models import User


# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(blank=True, upload_to='products_images')
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category}'

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def get_absolute_url(self):
        return reverse('web:update_product', args=[self.id])


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity
