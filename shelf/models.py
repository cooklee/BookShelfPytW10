from django.db import models


# Create your models here.
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


class Studio(models.Model):
    name = models.CharField(max_length=123)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.year}"
