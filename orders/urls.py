from django.urls import path

from orders.views import OrderCreateView, yookassa_webhook_view, OrdersListView

app_name = 'OnlineStore_orders'


urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('webhook', yookassa_webhook_view, name='webhook'),
    path('', OrdersListView.as_view(), name='orders_list')
]
