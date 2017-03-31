from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    pub_date = models.DateField()
    mod_date = models.DateField()
    body_text = models.TextField()

    def get_comment(self):
        id = self.id
        comments = Comment.objects.filter(blog_id=id)
        return comments

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    com_text = models.TextField()
    pub_date = models.DateField()

class Relatinship(models.Model):
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')