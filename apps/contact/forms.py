from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Форма обратной связи"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'company', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш email',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (___) ___-__-__',
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название компании',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тема сообщения',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше сообщение',
                'rows': 5,
                'required': True
            }),
        }
        labels = {
            'name': 'Имя',
            'email': 'Email',
            'phone': 'Телефон',
            'company': 'Компания',
            'subject': 'Тема',
            'message': 'Сообщение',
        }
    
    def clean_phone(self):
        """Валидация телефона"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Удаляем все символы кроме цифр и +
            cleaned_phone = ''.join(char for char in phone if char.isdigit() or char == '+')
            if len(cleaned_phone) < 10:
                raise forms.ValidationError('Введите корректный номер телефона')
        return phone
    
    def clean_email(self):
        """Валидация email"""
        email = self.cleaned_data.get('email')
        if email:
            # Простая проверка на наличие @ и точки
            if '@' not in email or '.' not in email.split('@')[-1]:
                raise forms.ValidationError('Введите корректный email адрес')
        return email
