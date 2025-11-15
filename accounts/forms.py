"""
Forms for accounts app.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, EmailVerification
from django.utils import timezone
from datetime import timedelta


class SignupForm(forms.ModelForm):
    """User signup form."""
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru'}),
        required=True
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        required=True
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = User
        fields = ['email']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают.')
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False  # Will be activated after email verification
        if commit:
            user.save()
        return user


class VerifyForm(forms.Form):
    """Email verification form."""
    code = forms.CharField(
        label='Код подтверждения',
        max_length=8,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите код из письма',
            'maxlength': '8',
            'autocomplete': 'off'
        }),
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not self.user:
            raise forms.ValidationError('Пользователь не найден.')
        
        try:
            verification = EmailVerification.objects.get(
                user=self.user,
                code=code,
                is_used=False
            )
        except EmailVerification.DoesNotExist:
            raise forms.ValidationError('Неверный код подтверждения.')
        
        if not verification.is_valid():
            raise forms.ValidationError('Код подтверждения истёк или уже использован.')
        
        return code


class LoginForm(AuthenticationForm):
    """Custom login form."""
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru', 'autofocus': True})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    error_messages = {
        'invalid_login': 'Введите правильный email и пароль.',
        'inactive': 'Этот аккаунт неактивен. Пожалуйста, подтвердите email.',
    }

