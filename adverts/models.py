"""
Models for adverts app.
"""
import os
import mimetypes
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse


def advert_media_path(instance, filename):
    """Путь для сохранения медиа файлов: /media/adverts/<user_id>/<filename>"""
    return f"adverts/{instance.owner_id}/{filename}"


class Category(models.Model):
    """Advertisement category model."""
    slug = models.SlugField(primary_key=True, max_length=50, verbose_name='Slug')
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Advert(models.Model):
    """Advertisement model."""
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        PUBLISHED = 'published', 'Опубликовано'
        ARCHIVED = 'archived', 'В архиве'
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='adverts',
        verbose_name='Автор'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='adverts',
        verbose_name='Категория'
    )
    title = models.CharField(max_length=120, verbose_name='Заголовок')
    body_md = models.TextField(verbose_name='Текст (Markdown)')
    body_html = models.TextField(verbose_name='Текст (HTML)', blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PUBLISHED,
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['author', '-created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('adverts:detail', kwargs={'pk': self.pk})


class MediaAsset(models.Model):
    """Media asset model for uploaded files (images and videos)."""
    IMAGE = 'image'
    VIDEO = 'video'
    TYPES = [
        (IMAGE, 'Изображение'),
        (VIDEO, 'Видео'),
    ]
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='media',
        verbose_name='Владелец'
    )
    file = models.FileField(upload_to=advert_media_path, verbose_name='Файл')
    type = models.CharField(
        max_length=10,
        choices=TYPES,
        default=IMAGE,
        verbose_name='Тип медиа'
    )
    mime = models.CharField(max_length=100, blank=True, verbose_name='MIME-тип')
    size = models.PositiveIntegerField(default=0, verbose_name='Размер (байт)')
    width = models.PositiveIntegerField(null=True, blank=True, verbose_name='Ширина (для изображений)')
    height = models.PositiveIntegerField(null=True, blank=True, verbose_name='Высота (для изображений)')
    poster = models.ImageField(upload_to=advert_media_path, null=True, blank=True, verbose_name='Постер (для видео)')
    duration = models.FloatField(null=True, blank=True, verbose_name='Длительность (секунды)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    
    class Meta:
        verbose_name = 'Медиафайл'
        verbose_name_plural = 'Медиафайлы'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if self.file:
            if not self.mime:
                self.mime = mimetypes.guess_type(self.file.name)[0] or ''
            self.size = getattr(self.file, 'size', 0)
            
            # Для изображений получаем размеры
            if self.type == self.IMAGE:
                try:
                    from PIL import Image
                    img = Image.open(self.file)
                    self.width, self.height = img.size
                except Exception:
                    pass
        
        super().save(*args, **kwargs)
    
    def filename(self):
        """Возвращает имя файла без пути"""
        return os.path.basename(self.file.name)
    
    def __str__(self):
        return f'{self.type}:{self.filename()}'
    
    @property
    def is_image(self):
        return self.type == self.IMAGE
    
    @property
    def is_video(self):
        return self.type == self.VIDEO

