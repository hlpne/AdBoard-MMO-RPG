"""
Services for adverts app.
"""
from markdown_it import MarkdownIt
import bleach
from django.conf import settings


def markdown_to_html(md_text):
    """
    Convert Markdown to HTML with safe sanitization.
    Поддерживает изображения и видео.
    """
    if not md_text:
        return ''
    
    # Use markdown-it-py for conversion
    md = MarkdownIt("commonmark")
    
    # Convert Markdown to HTML
    html = md.render(md_text)
    
    # Sanitize HTML with bleach - используем настройки из settings
    allowed_tags = getattr(settings, 'BLEACH_ALLOWED_TAGS', [
        'p', 'h1', 'h2', 'h3', 'h4', 'ul', 'ol', 'li', 'a', 'img', 'video',
        'blockquote', 'code', 'pre', 'strong', 'em', 'hr', 'br', 'source', 'figure', 'figcaption'
    ])
    
    allowed_attrs = getattr(settings, 'BLEACH_ALLOWED_ATTRS', {
        'a': ['href', 'title', 'rel', 'target'],
        'img': ['src', 'alt', 'title', 'width', 'height', 'class', 'style'],
        'video': ['controls', 'poster', 'preload', 'width', 'height', 'class', 'style'],
        'source': ['src', 'type'],
    })
    
    # Санитизация HTML через bleach с правильными настройками
    allowed_protocols = getattr(settings, 'BLEACH_ALLOWED_PROTOCOLS', ['http', 'https', 'mailto', 'data'])
    
    # Clean HTML - используем настройки из settings
    html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        protocols=allowed_protocols,
        strip=True,
        strip_comments=True
    )
    
    # Обрабатываем медиа файлы после конвертации Markdown и санитизации
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Add rel="nofollow noopener" to external links
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            if href.startswith('http') and 'rel' not in link.attrs:
                link['rel'] = 'nofollow noopener'
                if 'target' not in link.attrs:
                    link['target'] = '_blank'
        
        # Обрабатываем изображения - нормализуем пути и добавляем классы
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if not src:
                # Если src отсутствует, удаляем изображение
                img.decompose()
                continue
            
            # Проверяем, является ли это base64 data URI
            if src.startswith('data:'):
                # Base64 data URI - оставляем как есть, только добавляем класс
                pass
            elif src.startswith('/media/'):
                # Правильный путь - оставляем как есть
                pass
            elif not src.startswith('http') and not src.startswith('/'):
                # Относительный путь без слэша - добавляем /media/
                img['src'] = f'/media/{src}'
                src = img['src']
            
            # Добавляем класс для стилизации
            if 'class' not in img.attrs:
                img['class'] = []
            if isinstance(img['class'], list):
                if 'markdown-image' not in img['class']:
                    img['class'].append('markdown-image')
            elif isinstance(img['class'], str):
                img['class'] = ['markdown-image']
        
        # Обрабатываем видео теги
        for video in soup.find_all('video'):
            # Проверяем source теги внутри video
            sources = video.find_all('source')
            if sources:
                for source in sources:
                    src = source.get('src', '')
                    if src:
                        # Проверяем, является ли это base64 data URI
                        if src.startswith('data:'):
                            # Base64 data URI - оставляем как есть
                            pass
                        elif not src.startswith('http') and not src.startswith('/'):
                            # Относительный путь - добавляем /media/
                            source['src'] = f'/media/{src}'
            else:
                # Если нет source тегов, проверяем атрибут src у video
                src = video.get('src', '')
                if src:
                    # Проверяем, является ли это base64 data URI
                    if src.startswith('data:'):
                        # Base64 data URI - оставляем как есть
                        pass
                    elif not src.startswith('http') and not src.startswith('/'):
                        video['src'] = f'/media/{src}'
            
            # Добавляем controls если их нет
            if 'controls' not in video.attrs:
                video['controls'] = True
            
            # Добавляем класс
            if 'class' not in video.attrs:
                video['class'] = []
            if isinstance(video['class'], list):
                if 'markdown-video' not in video['class']:
                    video['class'].append('markdown-video')
            elif isinstance(video['class'], str):
                video['class'] = ['markdown-video']
        
        html = str(soup)
    except ImportError:
        # If BeautifulSoup is not available, skip processing
        pass
    
    return html


def search_adverts(query, queryset=None):
    """
    Search adverts by title and body.
    """
    from django.db import models as db_models
    from .models import Advert
    
    if queryset is None:
        queryset = Advert.objects.filter(status=Advert.Status.PUBLISHED)
    
    if query:
        queryset = queryset.filter(
            db_models.Q(title__icontains=query) | db_models.Q(body_md__icontains=query)
        )
    
    return queryset

