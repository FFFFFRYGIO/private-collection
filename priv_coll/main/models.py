from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="book", null=True)
    ISBN = models.BigIntegerField(null=False)
    title = models.CharField(max_length=270, null=False)
    authors = models.CharField(max_length=110, null=True, default=None, blank=True)
    publishedDate = models.CharField(max_length=10, null=True, default=None, blank=True)
    pageCount = models.IntegerField(null=True, default=None, blank=True)
    thumbnail = models.CharField(max_length=200, null=True, default=None, blank=True)
    language = models.CharField(max_length=10, null=True, default=None, blank=True)
    cost = models.FloatField(null=True, default=None, blank=True)

    class Meta:
        indexes = [models.Index(fields=["ISBN"])]
        constraints = [models.UniqueConstraint(fields=["user", "ISBN"], name="unique book assigment for user")]

    def __str__(self):
        return " ".join([str(self.user), str(self.ISBN), str(self.title)])
