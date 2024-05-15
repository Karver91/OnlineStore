from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from .models import EmailConfirmation, User
from .tasks import send_confirmation_email


class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    extra_context = {'title': 'Создать аккаунт'}

    def form_valid(self, form):
        user = form.save(commit=False)  # создание объекта без сохранения в БД
        user.set_password(form.cleaned_data['password1'])  # set_password шифрует пароль
        user.save()
        send_confirmation_email.delay(user_id=user.pk)
        return self._registration_confirmed()

    def _registration_confirmed(self):
        return render(self.request, 'users/registration_end.html', {
            'title': 'Подтверждение учетной записи',
            'container_header': 'Подтверждение учетной записи!',
            'container_body': 'Вам на почту отправлено письмо для подтверждения вашей учетной записи',
        })


class EmailConfirmationView(TemplateView):
    template_name = 'users/registration_end.html'
    extra_context = {
        'title': 'Регистрация прошла успешно',
        'container_header': 'Поздравляем!',
        'container_body': 'Вы успешно зарегистрировались!',
    }

    def get(self, request, *args, **kwargs):
        confirmation_code = kwargs['confirmation_code']
        email = kwargs['email']
        confirmation = get_object_or_404(EmailConfirmation, confirmation_code=confirmation_code)
        if confirmation:
            user = User.objects.get(email=email)
            user.is_confirmed = True
            user.save()
            confirmation.delete()
        return super().get(request, *args, **kwargs)


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True
    extra_context = {'title': 'Авторизация'}

    def form_valid(self, form):
        user = form.get_user()
        if user.is_confirmed:
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Ваша учетная запись еще не подтверждена.')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('OnlineStore_products:catalog')


class UserProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('OnlineStore_users:profile')
    extra_context = {
        'title': 'Профиль пользователя',
        'default_image': settings.DEFAULT_USER_IMAGE
    }

    def get_object(self, queryset=None):
        return self.request.user
