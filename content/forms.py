

from django import forms
from content.models import BlogPost


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "body","writer","category","thumbnail",]


        