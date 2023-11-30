from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200, default="", null=True, blank=True)
    image = models.ImageField(upload_to='post_image', default='6686925.jpg')
    body = models.TextField(default="", null=True, blank=True)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    no_of_likes = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user} - {self.title}'

    def likes_count(self):
        return self.post_votes.count()


class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')

    def __str__(self):
        return f'{self.user} liked {self.post}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_comment', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user}-{self.body[:20]}'
