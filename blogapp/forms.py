from django import forms
from .models import Comment




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Yorumunuzu buraya yazın...'
                })
        }

    def save(self, commit=True,request=None):
        comment = super().save(commit=False)
        if commit:
            comment.save()
        return comment