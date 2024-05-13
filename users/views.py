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


# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)  # создание объекта без сохранения в БД
#             user.set_password(form.cleaned_data['password1'])  # set_password шифрует пароль
#             user.save()
#             return render(request=request,
#                           template_name='users/registration_end.html',
#                           context={'title': 'Регистрация прошла успешно'})
#     else:
#         form = UserRegistrationForm()
#
#     context = {
#         'title': 'Создать аккаунт',
#         'form': form
#     }
#     return render(request=request, template_name='users/registration.html', context=context)
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


# def login_user(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request=request, user=user)
#                 return redirect('OnlineStore_products:catalog')
#     else:
#         form = UserLoginForm()
#     context = {'title': 'Авторизация', 'form': form}
#     return render(request=request, template_name='users/login.html', context=context)


# def logout_user(request):
#     logout(request)
#     return redirect('home')


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

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#     else:
#         form = UserProfileForm(instance=request.user)
#     context = {
#         'title': 'Профиль пользователя',
#         'default_image': settings.DEFAULT_USER_IMAGE,
#         'form': form
#     }
#     return render(request=request, template_name='users/profile.html', context=context)
