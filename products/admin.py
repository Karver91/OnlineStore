from django.contrib import admin

from .models import Product, Category, Size, Inventory

admin.site.register(Product)
admin.site.register(Size)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'quantity', 'product_price', 'product_category')
    list_display_links = ('product',)
    ordering = ('product__name', 'size')
    list_editable = ('quantity', )
    search_fields = ('product__name',)
    list_filter = ('product__category', 'size__size')

    @admin.display(description='Цена', ordering='product__price')
    def product_price(self, inventory: Inventory):
        return inventory.product.price

    @admin.display(description='Категория', ordering='product__category')
    def product_category(self, inventory: Inventory):
        return inventory.product.category

