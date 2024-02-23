from django.db import models
from django.contrib.auth.models import AbstractUser


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




class CourtType(models.Model):
   name = models.CharField(unique=True, db_index=True, max_length=100)


class Court(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  type = models.ForeignKey(CourtType, on_delete=models.CASCADE)
  state = models.ForeignKey(State, on_delete=models.CASCADE)
  title = models.CharField(max_length=155)
  description = models.TextField()
  price_per_hour = models.IntegerField()
  image = models.ImageField(upload_to='images/')
  open = models.TimeField()
  close = models.TimeField()
  location = models.URLField()

  # options
  closed_from = models.TimeField(null=True, blank=True)
  closed_to = models.TimeField(null=True, blank=True)

  closed_now = models.BooleanField(default=False, null=True, blank=True)

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
  court = models.ForeignKey(Court, on_delete=models.CASCADE, null=True, related_name='additional_court')


class CourtAdditionalTool(models.Model):
  court_additional = models.ForeignKey(CourtAdditional, on_delete=models.CASCADE, null=True, related_name='tools_court')
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
    court = Court.objects.get(pk=self.court.pk)
    selected_times = BookTime.objects.filter(book__pk=self.pk)
    settings = BookSetting.objects.get(book__pk=self.pk)

    price = 0

    if self.with_ball:
        price += court.ball_price * len(selected_times)

    if self.event:
        price += court.event_price * len(selected_times)

    if settings.tools:
       for i in settings.tools.all():
          price += i.price * len(selected_times)

    for time in selected_times:
        # offer
        if court.offer_price_per_hour is not None and court.offer_price_per_hour != 0 and str(court.offer_from)[:5] <= str(time.book_from) < str(court.offer_to)[:5]:
          price += court.offer_price_per_hour
        else:
          price += court.price_per_hour

    self.total_price = price

    super(Book, self).save(*args, **kwargs)

  def __str__(self):
      return self.name



class OverTime(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='book_over_time')
  book_from = models.TimeField(null=True, blank=True)
  book_to = models.TimeField(null=True, blank=True)
  note = models.TextField(null=True, blank=True)
  price = models.IntegerField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def save(self, *args, **kwargs):
    self.book.save()
    super(OverTime, self).save(*args, **kwargs)


class BookTime(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='book_time')
  book_from = models.TimeField(null=True)
  book_to = models.TimeField(null=True)
  book_to_date = models.DateField(null=True, blank=True)
  book_to_date_cancel = models.DateField(null=True, blank=True) #cancel spesific day

  def save(self, *args, **kwargs):
    self.book.save()
    super(BookTime, self).save(*args, **kwargs)


class BookSetting(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_setting')

  # addiotionals
  tools = models.ManyToManyField(CourtAdditionalTool, null=True, blank=True)

  def save(self, *args, **kwargs):
      self.book.save()
      super(BookSetting, self).save(*args, **kwargs)

