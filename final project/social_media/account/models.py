from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    age = models.CharField(default='1', null=True, blank=True, max_length=100)
    bio = models.TextField(blank=True, null=True, default='')
    profile_image = models.ImageField(upload_to='profile_image', default='Profile_icon.png')
    location = models.CharField(max_length=500, blank=True, null=True, default='')


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')

    def __str__(self):
        return f'{self.from_user} is following {self.to_user}'



