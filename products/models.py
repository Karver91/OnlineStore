from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Продукт')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='products_images', verbose_name='Фото')
    category = models.ForeignKey(
        to=Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products'
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ('name', )

    def __str__(self):
        return self.name


class Size(models.Model):
    size = models.CharField(max_length=4, verbose_name='Размер')

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"

    def __str__(self):
        return self.size


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='inventory')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name='Размер')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ('product__name', 'size')

    def __str__(self):
        return f'{self.size} | {self.product.name} | {self.quantity}'


class CartQuerySet(models.QuerySet):
    def get_total_price(self):
        return sum(product.get_product_sum() for product in self)


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Inventory, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartQuerySet.as_manager()

    def __str__(self):
        return f"User: {self.user} | Product: {self.product.product} | Size: {self.product.size} | Quantity: {self.quantity}"

    def get_product_sum(self):
        return self.product.product.price * self.quantity
