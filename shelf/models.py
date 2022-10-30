from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.urls import reverse


class Person(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title = models.CharField(max_length=123)
    year = models.IntegerField()
    director = models.ForeignKey(Person, on_delete=models.CASCADE)
    studio = models.ForeignKey('Studio', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title} {self.year} {self.director}"

    def get_absolute_url(self):
        return reverse('detail_movie', args=(self.id,))


class Studio(models.Model):
    name = models.CharField(max_length=123)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.year}"


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
