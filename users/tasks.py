from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.timezone import now

from users.models import User, EmailConfirmation


@shared_task
def send_confirmation_email(user_id):
    user = User.objects.get(pk=user_id)
    expiration = now() + timedelta(hours=24)
    confirmation = EmailConfirmation.objects.create(user=user, expiration=expiration)
    link = reverse('OnlineStore_users:email_confirmation', kwargs={
        'email': user.email,
        'confirmation_code': confirmation.confirmation_code
    })
    confirmation_link = f'{settings.DOMAIN_NAME}{link}'
    subject = f'Подтверждение учетной записи для {user.username}'
    message = f'Для подтверждения учетной записи {user.email} перейдите по ссылке: {confirmation_link}'
    from_email = settings.EMAIL_HOST_USER
    to_email = user.email
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=[to_email])
