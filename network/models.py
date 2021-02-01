from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Profile(models.Model):
    follower = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='following')
    following = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='follower')

    def __str__(self):
        return f"{self.follower} follows {self.following}"


class Post(models.Model):
    # Delete the post if it's user is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField()
    # Auto add the datetime when post is updated?
    date_added = models.DateTimeField(auto_now=True)
    liked_users = models.ManyToManyField(User, related_name='liked_posts')

    def __str__(self):
        return f"{self.user} {self.post} {self.date_added}"
