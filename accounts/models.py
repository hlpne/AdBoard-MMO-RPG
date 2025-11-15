"""
Models for accounts app.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import secrets
import string


class User(AbstractUser):
    """Custom User model with email as primary identifier."""
    email = models.EmailField(unique=True, verbose_name='Email')
    username = models.CharField(max_length=150, blank=True, null=True, verbose_name='Имя пользователя')
    is_active = models.BooleanField(default=False, verbose_name='Активен')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email


class EmailVerification(models.Model):
    """Email verification code model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verifications', verbose_name='Пользователь')
    code = models.CharField(max_length=8, verbose_name='Код подтверждения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    expires_at = models.DateTimeField(verbose_name='Истекает')
    is_used = models.BooleanField(default=False, verbose_name='Использован')
    
    class Meta:
        verbose_name = 'Подтверждение email'
        verbose_name_plural = 'Подтверждения email'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code', 'is_used']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        return f'{self.user.email} - {self.code}'
    
    @classmethod
    def generate_code(cls, length=6):
        """Generate random verification code."""
        characters = string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    def is_valid(self):
        """Check if verification code is valid."""
        return not self.is_used and timezone.now() < self.expires_at


class UserProfile(models.Model):
    """Optional user profile with additional information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    nickname = models.CharField(max_length=50, blank=True, verbose_name='Никнейм')
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True, verbose_name='Аватар')
    about = models.TextField(blank=True, verbose_name='О себе')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлён')
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f'Профиль {self.user.email}'

