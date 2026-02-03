from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['full_name', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше ФИО'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер телефона',
                'type': 'tel'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваш email'
            }),
        }
        error_messages = {
            'full_name': {
                'required': 'ФИО обязательно',
                'max_length': 'ФИО не должно превышать 200 символов',
            },
            'phone': {
                'required': 'Номер телефона обязателен',
                'max_length': 'Номер телефона не должен превышать 20 символов',
            },
            'email': {
                'required': 'Email обязателен',
                'invalid': 'Введите корректный email адрес',
            },
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].error_messages = {
            'required': 'ФИО обязательно',
            'max_length': 'ФИО не должно превышать 200 символов',
        }
        self.fields['phone'].error_messages = {
            'required': 'Номер телефона обязателен',
            'max_length': 'Номер телефона не должен превышать 20 символов',
        }
        self.fields['email'].error_messages = {
            'required': 'Email обязателен',
            'invalid': 'Введите корректный email адрес',
        }

