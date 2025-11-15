"""
Models for newsletters app.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone


class Subscription(models.Model):
    """Newsletter subscription model."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='newsletter_subscription',
        verbose_name='Пользователь'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')
    
    class Meta:
        verbose_name = 'Подписка на рассылку'
        verbose_name_plural = 'Подписки на рассылки'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Подписка {self.user.email}'


class NewsletterTemplate(models.Model):
    """Newsletter template model."""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    html_body = models.TextField(verbose_name='HTML-тело письма')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    
    class Meta:
        verbose_name = 'Шаблон рассылки'
        verbose_name_plural = 'Шаблоны рассылок'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class NewsletterSendJob(models.Model):
    """Newsletter send job model."""
    class Status(models.TextChoices):
        QUEUED = 'queued', 'В очереди'
        SENDING = 'sending', 'Отправляется'
        DONE = 'done', 'Завершена'
        FAILED = 'failed', 'Ошибка'
    
    template = models.ForeignKey(
        NewsletterTemplate,
        on_delete=models.CASCADE,
        related_name='send_jobs',
        verbose_name='Шаблон'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.QUEUED,
        verbose_name='Статус'
    )
    total = models.IntegerField(default=0, verbose_name='Всего получателей')
    sent = models.IntegerField(default=0, verbose_name='Отправлено')
    errors = models.IntegerField(default=0, verbose_name='Ошибок')
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='Начало отправки')
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name='Окончание отправки')
    
    class Meta:
        verbose_name = 'Задача рассылки'
        verbose_name_plural = 'Задачи рассылок'
        ordering = ['-started_at']
    
    def __str__(self):
        return f'Рассылка {self.template.title} - {self.status}'

