from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'book', 'image']
        labels = {
            'image': _('رابط الصورة')
        }
        widgets = {
            'image': forms.widgets.URLInput
        }