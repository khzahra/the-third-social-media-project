from django import forms
from .models import Post, Comment


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image',  'body')


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
