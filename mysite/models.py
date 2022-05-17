from django.db import models

class Item(models.Model):
  name = models.CharField(max_length=10)
  code = models.CharField(max_length=10)

class User(models.Model):
  email = models.CharField(max_length=30, primary_key=True)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  

class Movie(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    stock = models.IntegerField(default=1)

class Rentals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
