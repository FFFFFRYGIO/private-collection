from django.db import models

# Create your models here.


class Book(models.Model):
    ISBN = models.CharField(max_length=50, null=False, unique=True)
    title = models.CharField(max_length=270, null=False)
    authors = models.CharField(max_length=110, null=False)
    publishedDate = models.CharField(max_length=10, null=True, default=None, blank=True)
    pageCount = models.IntegerField(null=True, default=None, blank=True)
    thumbnail = models.CharField(max_length=200, null=True, default=None, blank=True)
    language = models.CharField(max_length=10, null=True, default=None, blank=True)
    slug = models.SlugField(max_length=4, unique=True)
    class Meta:
        indexes = [
            models.Index(fields=['ISBN'])
        ]

    def __str__(self):
        return " ".join([str(self.ISBN), str(self.title)])
