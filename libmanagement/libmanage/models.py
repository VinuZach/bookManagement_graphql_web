from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class AuthorDetails(models.Model):
    name = models.CharField(null=False, max_length=30)
    star_rating = models.IntegerField(default=0, validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(null=False, max_length=20)

    def __str__(self):
        return self.name


class Books(models.Model):
    AVAILABILITY = {
        "NA": "Not Available",
        "A": "Available",
        "L": "Lent",
        "R": "Reserved",
        "Up": "Upcoming"
    }
    title = models.CharField(null=False, max_length=20)
    author = models.ForeignKey(AuthorDetails, default=1, on_delete=models.PROTECT,related_name="author")
    availability_status = models.CharField(null=False, choices=AVAILABILITY,max_length=5)
    genre = models.ForeignKey(Genre, default=1, on_delete=models.PROTECT)

    def __str__(self):
        return self.title