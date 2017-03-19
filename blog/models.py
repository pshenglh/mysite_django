from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Blog(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    pub_date = models.DateField()
    mod_date = models.DateField()
    body_text = models.TextField()

    def __str__(self):
        return self.title

class comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    com_text = models.TextField()
    pub_date = models.DateField()