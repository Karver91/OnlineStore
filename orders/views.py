import json
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, ListView
from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory

from orders.form import OrderForm
from orders.models import Order
from products.models import Cart

# Yookassa
Configuration.configure(account_id=settings.YOOKASSA_SHOP_ID, secret_key=settings.YOOKASSA_SECRET_KEY)


class OrderCreateView(LoginRequiredMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('OnlineStore_products:catalog')
    extra_context = {'title': 'Оформление заказа'}

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        # Вызываем метод form_valid() из родительского класса для сохранения объекта заказа
        super().form_valid(form)
        # Создаем платеж и перенаправляем на страницу подтверждения
        cart = Cart.objects.filter(user=self.request.user)
        amount = cart.get_total_price()
        payment = Payment.create(
            {
                "amount": {
                    "value": f'{amount}',
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": f'{settings.DOMAIN_NAME}{self.success_url}'
                },
                "capture": True,
                "test": True,
                "description": f"Заказ №{self.object.id}",
                "metadata": {
                    'orderNumber': f'{self.object.id}'
                }
            }
        )
        return HttpResponseRedirect(payment.confirmation.confirmation_url, status=HTTPStatus.SEE_OTHER)


@csrf_exempt
def yookassa_webhook_view(request):
    # Извлечение JSON объекта из тела запроса
    event_json = json.loads(request.body)
    try:
        # Создание объекта класса уведомлений в зависимости от события
        notification_object = WebhookNotificationFactory().create(event_json)
        response_object = notification_object.object
        order_id = response_object.metadata.get('orderNumber')
        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            order = Order.objects.get(id=order_id)
            order.update_after_payment()
        elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
            order = Order.objects.get(id=order_id)
            order.delete()
        else:
            return HttpResponse(status=400)  # Сообщаем кассе об ошибке
    except Exception:
        return HttpResponse(status=400)  # Сообщаем кассе об ошибке

    return HttpResponse(status=200)  # Сообщаем кассе, что все хорошо


class OrdersListView(LoginRequiredMixin, ListView):
    template_name = 'orders/orders.html'
    extra_context = {'title': 'Заказы'}
    queryset = Order.objects.all()
    ordering = ('-id', )

    def get_queryset(self):
        queryset = super().get_queryset().filter(initiator=self.request.user)
        queryset.filter(status=0).delete()
        return queryset
