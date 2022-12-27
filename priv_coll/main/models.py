from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book', null=True)
    ISBN = models.CharField(max_length=50, null=False, unique=True)
    title = models.CharField(max_length=270, null=False)
    authors = models.CharField(max_length=110, null=False)
    publishedDate = models.CharField(max_length=10, null=True, default=None, blank=True)
    pageCount = models.IntegerField(null=True, default=None, blank=True)
    thumbnail = models.CharField(max_length=200, null=True, default=None, blank=True)
    language = models.CharField(max_length=10, null=True, default=None, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['ISBN'])
        ]

    def __str__(self):
        return " ".join([str(self.ISBN), str(self.title)])
