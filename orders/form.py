from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={
        'placeholder': 'Иван'
    }))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={
        'placeholder': 'Иванов'
    }))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={
        'placeholder': 'you@mail.com'
    }))
    address = forms.CharField(label='Адрес', widget=forms.TextInput(attrs={
        'placeholder': 'Россия, Калининград, пр. Мира, дом 6'
    }))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')
