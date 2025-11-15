"""
Forms for adverts app.
"""
import base64
import mimetypes
from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import Advert, Category
from .services import markdown_to_html


class AdvertForm(forms.ModelForm):
    """Advertisement form with Markdown editor and base64 media upload."""
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        empty_label='Выберите категорию'
    )
    title = forms.CharField(
        label='Заголовок',
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
        required=True
    )
    body_md = forms.CharField(
        label='Текст объявления',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 15,
            'placeholder': 'Введите текст объявления. Поддерживается форматирование Markdown.'
        }),
        required=True,
        help_text=''
    )
    upload_image = forms.ImageField(
        label='Загрузить изображение',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/png,image/jpeg,image/webp,image/gif',
            'id': 'id_upload_image'
        }),
        help_text=f'Максимальный размер: {getattr(settings, "MAX_IMAGE_SIZE_MB", 10)} МБ'
    )
    upload_video = forms.FileField(
        label='Загрузить видео',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'video/mp4,video/webm',
            'id': 'id_upload_video'
        }),
        help_text=f'Максимальный размер: {getattr(settings, "MAX_VIDEO_SIZE_MB", 100)} МБ'
    )
    
    class Meta:
        model = Advert
        fields = ['category', 'title', 'body_md']
    
    def clean_upload_image(self):
        """Validate image file size."""
        image = self.cleaned_data.get('upload_image')
        if image:
            max_size_mb = getattr(settings, 'MAX_IMAGE_SIZE_MB', 10)
            max_size_bytes = max_size_mb * 1024 * 1024
            
            if image.size > max_size_bytes:
                raise ValidationError(
                    f'Размер изображения превышает {max_size_mb} МБ. '
                    f'Текущий размер: {image.size / (1024 * 1024):.2f} МБ'
                )
            
            # Проверка MIME типа
            mime_type = mimetypes.guess_type(image.name)[0]
            allowed_types = ['image/png', 'image/jpeg', 'image/webp', 'image/gif']
            if mime_type not in allowed_types:
                raise ValidationError(
                    f'Недопустимый формат изображения. Разрешены: PNG, JPEG, WebP, GIF'
                )
        
        return image
    
    def clean_upload_video(self):
        """Validate video file size."""
        video = self.cleaned_data.get('upload_video')
        if video:
            max_size_mb = getattr(settings, 'MAX_VIDEO_SIZE_MB', 100)
            max_size_bytes = max_size_mb * 1024 * 1024
            
            if video.size > max_size_bytes:
                raise ValidationError(
                    f'Размер видео превышает {max_size_mb} МБ. '
                    f'Текущий размер: {video.size / (1024 * 1024):.2f} МБ'
                )
            
            # Проверка MIME типа
            mime_type = mimetypes.guess_type(video.name)[0]
            allowed_types = ['video/mp4', 'video/webm']
            if mime_type not in allowed_types:
                raise ValidationError(
                    f'Недопустимый формат видео. Разрешены: MP4, WebM'
                )
        
        return video
    
    def _file_to_base64(self, file_field, file_type='image'):
        """Convert uploaded file to base64 data URI."""
        if not file_field:
            return None
        
        file_field.seek(0)  # Reset file pointer
        file_content = file_field.read()
        base64_content = base64.b64encode(file_content).decode('utf-8')
        
        # Determine MIME type
        mime_type = mimetypes.guess_type(file_field.name)[0]
        if not mime_type:
            # Fallback based on file type
            if file_type == 'image':
                mime_type = 'image/png'
            else:
                # Try to determine from content_type if available
                if hasattr(file_field, 'content_type') and file_field.content_type:
                    mime_type = file_field.content_type
                else:
                    mime_type = 'video/mp4'
        elif file_type == 'video' and mime_type not in ['video/mp4', 'video/webm']:
            # Ensure video MIME type is correct
            if hasattr(file_field, 'content_type') and file_field.content_type:
                mime_type = file_field.content_type
        
        # Create data URI
        data_uri = f'data:{mime_type};base64,{base64_content}'
        return data_uri
    
    def _insert_media_to_markdown(self, body_md, image_data_uri=None, video_data_uri=None):
        """Insert base64 media into Markdown text."""
        if not image_data_uri and not video_data_uri:
            return body_md
        
        # Find cursor position (end of text) or insert at the end
        lines_to_add = []
        
        if image_data_uri:
            # Insert image as Markdown
            lines_to_add.append(f'\n\n![Изображение]({image_data_uri})\n')
        
        if video_data_uri:
            # Extract MIME type from data URI
            mime_type = 'video/mp4'  # default
            if 'data:' in video_data_uri and ';base64,' in video_data_uri:
                mime_part = video_data_uri.split('data:')[1].split(';base64,')[0]
                if mime_part:
                    mime_type = mime_part
            
            # Insert video as HTML (Markdown doesn't support video well)
            lines_to_add.append(f'\n\n<video controls><source src="{video_data_uri}" type="{mime_type}"></video>\n')
        
        # Append to body_md
        return body_md + ''.join(lines_to_add)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Process uploaded media files
        image = self.cleaned_data.get('upload_image')
        video = self.cleaned_data.get('upload_video')
        
        if image or video:
            # Convert files to base64 and insert into Markdown
            image_data_uri = None
            video_data_uri = None
            
            if image:
                image_data_uri = self._file_to_base64(image, 'image')
            
            if video:
                video_data_uri = self._file_to_base64(video, 'video')
            
            # Insert media into body_md
            instance.body_md = self._insert_media_to_markdown(
                instance.body_md,
                image_data_uri,
                video_data_uri
            )
        
        # Convert Markdown to HTML
        instance.body_html = markdown_to_html(instance.body_md)
        
        if commit:
            instance.save()
        
        return instance
