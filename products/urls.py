from django.urls import path

from products.views import remove_product_from_cart, CatalogView, ProductDetailView, CartView

app_name = 'OnlineStore_products'


urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/remove/<int:cart_id>/', remove_product_from_cart, name='product_remove'),
    path('catalog/all/', CatalogView.as_view(), name='catalog'),
    path('catalog/<slug:slug>/', CatalogView.as_view(), name='category_by_slug'),
    path('catalog/<slug:slug>/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
]
