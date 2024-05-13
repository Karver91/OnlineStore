import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя пользователя'
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль'
    }))

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={
        'placeholder': 'Введите фамилию'
    }))
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя пользователя'
    }))
    email = forms.CharField(label='Адрес электронной почты', widget=forms.EmailInput(attrs={
        'placeholder': 'Введите адрес эл. почты'
    }))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={
        'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    this_year = datetime.date.today().year

    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={
        'class': 'form-input'
    }))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={
        'class': 'form-input'
    }))
    email = forms.CharField(label='Электронный адрес',
                            disabled=True,
                            required=False,
                            widget=forms.TextInput(attrs={
                                'class': 'form-input', 'readonly': True
                            }))
    date_birth = forms.DateField(label='Дата рождения',
                                 widget=forms.SelectDateWidget(years=tuple(range(this_year - 100, this_year - 3))))
    photo = forms.ImageField(label='Фотография профиля',
                             required=False,
                             widget=forms.FileInput(attrs={
                                 'class': 'custom-file-input',
                             }))
    username = forms.CharField(label='Имя пользователя',
                               disabled=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-input'
                               }))

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'date_birth', 'photo')
