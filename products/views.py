from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView

from .models import Product, Category, Cart, Inventory


class IndexView(TemplateView):
    template_name = 'products/index.html'
    extra_context = {'title': 'OnlineStore'}


# def index(request):
#     return render(request=request, template_name='products/index.html', context={'title': 'Online Store'})


class CatalogView(ListView):
    model = Product
    template_name = 'products/catalog.html'
    context_object_name = 'products'
    paginate_by = 3

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.categories = Category.objects.all()
        self.title = 'Каталог товаров'

    def get_queryset(self):
        slug = self.kwargs.get('slug')

        if slug:
            category = get_object_or_404(self.categories, slug=slug)  # Получаем категорию по слагу из списка категорий
            self.title = category.name
            return Product.objects.filter(inventory__quantity__gt=0, category=category).annotate(
                num_products=Count('id')).order_by('id')
        return Product.objects.filter(inventory__quantity__gt=0).annotate(num_products=Count('id')).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['categories'] = self.categories
        self.request.session['catalog_url'] = self.request.get_full_path()
        return context


# def catalog(request):
#     products = Product.objects.filter(inventory__quantity__gt=0).annotate(num_products=Count('id')).order_by('id')
#     products_paginator = _get_paginator(object_list=products, page=request.GET.get('page'))
#     context = {
#         'title': 'Каталог товаров',
#         'categories': Category.objects.all(),
#         'products': products_paginator
#     }
#     request.session['catalog_url'] = request.path
#     return render(request=request, template_name='products/catalog.html', context=context)
#
#
# def category_by_slug(request, slug):
#     categories = Category.objects.all()
#     category = get_object_or_404(categories, slug=slug)  # Получаем категорию по слагу из списка категорий
#     products = Product.objects.filter(inventory__quantity__gt=0, category=category).annotate(
#         num_products=Count('id')).order_by('id')  # Получаем список продуктов по категории
#     products_paginator = _get_paginator(object_list=products, page=request.GET.get('page'))
#     context = {
#         'title': category.name,
#         'categories': categories,
#         'products': products_paginator
#     }
#     request.session['catalog_url'] = request.path
#     return render(request=request, template_name='products/catalog.html', context=context)
#
#
# def _get_paginator(object_list, page):
#     paginator = Paginator(object_list=object_list, per_page=6)
#     page = page if page else 1
#     return paginator.page(page)


class ProductDetailView(LoginRequiredMixin, ListView):
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        self.queryset = Inventory.objects.filter(product=product_id, quantity__gt=0)
        self.product = self.queryset.first()
        return self.queryset

    def post(self, request, *args, **kwargs):
        catalog_url = request.session.get(key='catalog_url', default=reverse_lazy('OnlineStore_products:catalog'))
        product_id = self.kwargs.get('product_id')
        queryset = Inventory.objects.filter(product=product_id, quantity__gt=0)
        self._add_product_to_cart(products=queryset)
        return render(request=request,
                      template_name='products/product_add_success.html',
                      context={'catalog_url': catalog_url})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.product.product.name
        return context

    def _add_product_to_cart(self, products) -> None:
        selected_size = self.request.POST.get('size')
        selected_product = products.get(size__size=selected_size)
        user_cart_product = Cart.objects.filter(user=self.request.user, product=selected_product)

        if not user_cart_product.exists():  # если в корзине отсутствуют этот продукт
            Cart.objects.create(user=self.request.user, product=selected_product, quantity=1)
        else:
            user_cart_product = user_cart_product.first()
            user_cart_product.quantity += 1
            user_cart_product.save()

        selected_product.quantity -= 1  # убираем товар из инвентаря
        selected_product.save()
        return None


# @login_required
# def product_detail(request, slug, product_id):
#     product = Inventory.objects.filter(product=product_id, quantity__gt=0)
#
#     if request.method == 'POST':
#         catalog_url = request.session.get(key='catalog_url', default=reverse('OnlineStore_products:catalog'))
#         _add_product_to_cart(request=request, product=product)
#         return render(request=request,
#                       template_name='products/product_add_success.html',
#                       context={'catalog_url': catalog_url})
#
#     return render(request, 'products/product_detail.html', {'product': product})
#
#
# def _add_product_to_cart(request, product) -> None:
#     selected_size = request.POST.get('size')
#     selected_product = product.get(size__size=selected_size)
#     user_cart_product = Cart.objects.filter(user=request.user, product=selected_product)
#
#     if not user_cart_product.exists():  # если в корзине отсутствуют этот продукт
#         Cart.objects.create(user=request.user, product=selected_product, quantity=1)
#     else:
#         user_cart_product = user_cart_product.first()
#         user_cart_product.quantity += 1
#         user_cart_product.save()
#
#     selected_product.quantity -= 1  # убираем товар из инвентаря
#     selected_product.save()
#
#     return None


class CartView(LoginRequiredMixin, ListView):
    template_name = 'products/cart.html'
    context_object_name = 'cart'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзина'
        context['catalog_url'] = self.request.session.get(key='catalog_url', default=reverse_lazy('OnlineStore_products:catalog'))
        return context


# @login_required
# def cart_view(request):
#     catalog_url = request.session.get(key='catalog_url', default=reverse('OnlineStore_products:catalog'))
#     user_cart = Cart.objects.filter(user=request.user)
#     context = {
#         'cart': user_cart,
#         'catalog_url': catalog_url,
#     }
#     return render(request=request, template_name='products/cart.html', context=context)


@login_required
def remove_product_from_cart(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
