"""
Models for replies app.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone


class Reply(models.Model):
    """Reply to an advert model."""
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает рассмотрения'
        ACCEPTED = 'accepted', 'Принят'
        DELETED = 'deleted', 'Удалён'
    
    advert = models.ForeignKey(
        'adverts.Advert',
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name='Объявление'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name='Автор отклика'
    )
    text = models.TextField(verbose_name='Текст отклика')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлён')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Удалён')
    
    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['advert', 'status', '-created_at']),
            models.Index(fields=['author', '-created_at']),
        ]
    
    def __str__(self):
        return f'Отклик от {self.author.email} на "{self.advert.title}"'

