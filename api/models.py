from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class State(models.Model):
    name = models.CharField(max_length=155,null=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    phone = models.IntegerField(null=True)

    def __str__(self):
        return self.username




class Court(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
  state = models.ForeignKey(State, on_delete=models.CASCADE,null=True)
  title = models.CharField(max_length=155,null=True)
  description = models.TextField(null=True)
  price_per_hour = models.IntegerField(null=True)
  image = models.ImageField(upload_to='images/',null=True)
  open = models.TimeField(null=True)
  close = models.TimeField(null=True)
  # options
  offer_price_per_hour = models.IntegerField(null=True, blank=True)
  offer_from = models.TimeField(null=True, blank=True)
  offer_to = models.TimeField(null=True, blank=True)
  with_ball = models.BooleanField(default=True,null=True)
  ball_price = models.IntegerField(null=True, blank=True)
  event = models.BooleanField(default=False,null=True)
  event_price = models.IntegerField(null=True, blank=True)
  event_from = models.TimeField(null=True, blank=True)
  event_to = models.TimeField(null=True, blank=True)
  location = models.URLField(null=True)


  def __str__(self):
      return self.title



class CourtAdditional(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
  court = models.ForeignKey(Court, on_delete=models.CASCADE, null=True)

class CourtAdditionalTool(models.Model):
  court_additional = models.ForeignKey(CourtAdditional, on_delete=models.CASCADE, null=True)
  title = models.CharField(max_length=255)
  price = models.IntegerField()
  




class Book(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
  court = models.ForeignKey(Court, on_delete=models.CASCADE, null=True)
  name = models.CharField(max_length=255)
  phone = models.CharField(max_length=255)
  book_date = models.DateField()
  book_from = models.TimeField()
  book_to = models.TimeField()
  with_ball = models.BooleanField()
  event = models.BooleanField()
  total_price = models.IntegerField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


  def save(self, *args, **kwargs):
      self.total_price = self.court.price_per_hour

      if self.with_ball:
         self.total_price += self.court.ball_price

      if self.event:
         self.total_price += self.court.event_price

      # check if offer made
      super(Book, self).save(*args, **kwargs)

  def __str__(self):
      return self.name



class BookSetting(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE)

  # book to specific date
  book_to = models.DateField(null=True, blank=True)

  # addiotionals
  tools = models.ManyToManyField(CourtAdditionalTool, null=True, blank=True)

