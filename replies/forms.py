"""
Forms for replies app.
"""
from django import forms
from .models import Reply


class ReplyForm(forms.ModelForm):
    """Reply form."""
    text = forms.CharField(
        label='Текст отклика',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Введите текст отклика'
        }),
        required=True,
        max_length=2000
    )
    
    class Meta:
        model = Reply
        fields = ['text']
    
    def __init__(self, *args, **kwargs):
        self.advert = kwargs.pop('advert', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Check if user is trying to reply to their own advert
        if self.advert and self.user and self.advert.author == self.user:
            raise forms.ValidationError('Вы не можете оставить отклик на своё объявление.')
        
        return cleaned_data

