from django.db import models
from django.contrib.auth.models import User


class BlogUser(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(to=BlogUser, on_delete=models.CASCADE)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    user = models.ForeignKey(to=BlogUser, on_delete=models.CASCADE)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class File(models.Model):
    file = models.FileField(upload_to="files/", null=True, blank=True)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name


class Block(models.Model):
    blocker = models.ForeignKey(to=BlogUser, on_delete=models.CASCADE, related_name="user_blocker")
    blocked = models.ForeignKey(to=BlogUser, on_delete=models.CASCADE, related_name="user_blocked")

    def __str__(self):
        return str(self.blocker) + " blocked " + str(self.blocked)
