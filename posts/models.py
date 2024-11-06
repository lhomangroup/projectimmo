from django.db import models

class Post(models.Model):
    objects = None
    title = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.title

class PostImage(models.Model):
    objects = None
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to = 'images/')

    def __str__(self):
        return self.post.title

