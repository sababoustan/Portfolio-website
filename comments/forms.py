from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نظر خود را بنویسید...',
                'rows': 4
            }),            
        }