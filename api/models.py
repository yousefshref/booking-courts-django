from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

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
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  state = models.ForeignKey(State, on_delete=models.CASCADE)
  title = models.CharField(max_length=155)
  description = models.TextField()
  price_per_hour = models.IntegerField()
  image = models.ImageField(upload_to='images/')
  open = models.TimeField()
  close = models.TimeField()
  location = models.URLField()
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


  def __str__(self):
      return str(self.title)



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
  with_ball = models.BooleanField()
  event = models.BooleanField()
  total_price = models.IntegerField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


  def save(self, *args, **kwargs):
      super(Book, self).save(*args, **kwargs)

  def __str__(self):
      return self.name


class BookTime(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='book_time')
  book_from = models.TimeField(null=True)
  book_to = models.TimeField(null=True)
   


class BookSetting(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE)

  # book to specific date
  book_to = models.DateField(null=True, blank=True)

  # addiotionals
  tools = models.ManyToManyField(CourtAdditionalTool, null=True, blank=True)

  def save(self, *args, **kwargs):
      self.book.save()
      super(BookSetting, self).save(*args, **kwargs)
