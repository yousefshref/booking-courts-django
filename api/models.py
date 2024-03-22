from django.db import models
from django.contrib.auth.models import AbstractUser

import subprocess
from django.db.models import Q
from datetime import time, timedelta, datetime
from django.db.models import Sum


# functions
def get_hours_between(start_time, end_time):
  """
  This function takes two times in the format "HH:MM:SS" and returns a list of hours between them.

  Args:
      start_time: The start time in the format "HH:MM:SS".
      end_time: The end time in the format "HH:MM:SS".

  Returns:
      A list of hours between the start and end time, inclusive.
  """
  start_datetime = datetime.strptime(start_time, "%H:%M:%S")
  end_datetime = datetime.strptime(end_time, "%H:%M:%S")

  # Handle the case where the start time is after the end time
  if start_datetime > end_datetime:
    end_datetime = end_datetime + timedelta(days=1)

  hours = []
  current_time = start_datetime
  while current_time <= end_datetime:
    hours.append(current_time.strftime("%H"))
    current_time += timedelta(hours=1)

  return hours




class State(models.Model):
    name = models.CharField(max_length=155,null=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    phone = models.IntegerField(null=True, unique=True, db_index=True)

    # staff
    staff_for = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=True, blank=True, related_name='staff_for_user')

    # wallet infos
    x_pay_phone = models.IntegerField(null=True, unique=True, db_index=True, blank=True)
    x_pay_password = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
      super(CustomUser, self).save(*args, **kwargs)



class CourtType(models.Model):
  name = models.CharField(unique=True, db_index=True, max_length=100)

class CourtTypeT(models.Model):
  name = models.CharField(unique=True, db_index=True, max_length=100)


class Court(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_court')
  type = models.ForeignKey(CourtType, on_delete=models.CASCADE, null=True)
  type2 = models.ForeignKey(CourtTypeT, on_delete=models.CASCADE, null=True)
  state = models.ForeignKey(State, on_delete=models.CASCADE)
  title = models.CharField(max_length=155)
  description = models.TextField()
  price_per_hour = models.IntegerField()
  # image = models.ImageField(upload_to='images/')
  open = models.TimeField()
  close = models.TimeField()
  location = models.URLField()

  # options
  closed_from = models.TimeField(null=True, blank=True)
  closed_to = models.TimeField(null=True, blank=True)

  closed_now = models.BooleanField(default=False, null=True, blank=True)

  offer_price_per_hour = models.IntegerField(default=0, null=True, blank=True)
  offer_from = models.TimeField(null=True, blank=True)
  offer_to = models.TimeField(null=True, blank=True)
  with_ball = models.BooleanField(default=False,null=True)
  ball_price = models.IntegerField(default=0, null=True, blank=True)
  event = models.BooleanField(default=False,null=True)
  event_price = models.IntegerField(default=0, null=True, blank=True)
  event_from = models.TimeField(null=True, blank=True)
  event_to = models.TimeField(null=True, blank=True)



  def round_to_nearest_hour(self, time):
      # Calculate the minutes and seconds portion of the time
      total_seconds = time.hour * 3600 + time.minute * 60 + time.second
      # Round to the nearest hour
      rounded_seconds = round(total_seconds / 3600) * 3600
      # Convert back to hours, minutes, and seconds
      rounded_time = timedelta(seconds=rounded_seconds)
      return rounded_time

  def save(self, *args, **kwargs):
    if self.ball_price == 0 and self.with_ball:
      self.with_ball = False

    if self.event_price == 0 and self.event:
      self.event = False

    if self.offer_price_per_hour == 0 and self.offer_from:
      self.offer_from = None
      self.offer_to = None

    self.open = str(self.round_to_nearest_hour(self.open))
    self.close = str(self.round_to_nearest_hour(self.close))

    self.title = self.title.split('_')[0]

    if self.offer_price_per_hour is not None and self.offer_price_per_hour > 0:
        # Convert positive value to negative
        self.offer_price_per_hour *= -1


    if self.open > self.close:
        # Swap the values
        self.open, self.close = self.close, self.open

    super(Court, self).save(*args, **kwargs)


  def __str__(self):
      return str(self.title)




class CourtFeature(models.Model):
  court = models.ForeignKey(Court, on_delete=models.CASCADE, null=True, related_name='court_features')
  feature = models.CharField(max_length=155)
  is_free = models.BooleanField(default=False)
  is_available = models.BooleanField(null=True, default=True)




class CourtImage(models.Model):
  court = models.ForeignKey(Court, on_delete=models.CASCADE, null=True, related_name='court_image')
  image = models.ImageField(upload_to='courts/images/', null=True, blank=True)


class CourtVideo(models.Model):
  court = models.ForeignKey(Court, on_delete=models.CASCADE, null=True, related_name='court_video')
  video = models.FileField(upload_to='videos/', null=True, blank=True)




class CourtAdditional(models.Model):
  court = models.ForeignKey(Court, on_delete=models.CASCADE, null=True, related_name='additional_court')


class CourtAdditionalTool(models.Model):
  court_additional = models.ForeignKey(CourtAdditional, on_delete=models.CASCADE, null=True, related_name='tools_court')
  title = models.CharField(max_length=255)
  price = models.IntegerField()






paied_choices = (
   ('عند الوصول', 'عند الوصول'),
   ('محفظة الكترونية', 'محفظة الكترونية'),
)

class Book(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
  court = models.ForeignKey(Court, on_delete=models.CASCADE, null=True)
  name = models.CharField(max_length=255)
  phone = models.CharField(max_length=255)
  book_date = models.DateField()

  total_price = models.IntegerField(null=True, blank=True, default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)



  def __str__(self):
      return self.name



class BookTime(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='book_time')
  book_from = models.TimeField(null=True, blank=True)
  book_to = models.TimeField(null=True, blank=True)
  book_to_date = models.DateField(null=True, blank=True)

  with_ball = models.BooleanField(default=False, null=True, blank=True)
  event = models.BooleanField(default=False, null=True, blank=True)
  paied = models.CharField(max_length=155, choices=paied_choices, null=True, blank=True)
  is_paied = models.BooleanField(default=False, null=True, blank=True)
  is_cancelled = models.BooleanField(default=False, null=True, blank=True)
  is_cancelled_day = models.DateField(null=True, blank=True)
  tools = models.ManyToManyField(CourtAdditionalTool, null=True, blank=True)
  total_price = models.IntegerField(null=True, blank=True, default=0)

  def get_total_price(self):
    total = 0
    # ball
    if self.book.court.ball_price > 0 and self.with_ball == 'True':
      total += self.book.court.ball_price

    # tools
    for i in self.tools.all():
      total += i.price

    try:
      event_range = get_hours_between(str(self.book.court.event_from), str(self.book.court.event_to))
      # event
      if self.book.court.event_price and self.event == 'True' and str(self.book_from)[0:2] in event_range and str(self.book_to)[0:2] in event_range:
        total += self.book.court.event_price
    except:
      pass
    try:
      offer_range = get_hours_between(str(self.book.court.offer_from), str(self.book.court.offer_to))
      # offer
      if self.book.court.offer_price_per_hour and str(self.book_from)[0:2] in offer_range and str(self.book_to)[0:2] in offer_range:
        total += self.book.court.offer_price_per_hour
    except:
      pass

    # normal
    total += self.book.court.price_per_hour

    self.total_price = total


  def save(self, *args, **kwargs):
    super(BookTime, self).save(*args, **kwargs)  # Save the instance
    self.get_total_price()
    super(BookTime, self).save(*args, **kwargs)  # Save the instance


from django.db.models.signals import m2m_changed
from django.dispatch import receiver
@receiver(m2m_changed, sender=BookTime.tools.through)
def update_total_sum(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.save()

class OverTime(models.Model):
  book = models.ForeignKey(Book, unique=True, db_index=True, on_delete=models.CASCADE, null=True, related_name='book_over_time')
  book_from = models.TimeField(null=True, blank=True)
  book_to = models.TimeField(null=True, blank=True)
  note = models.TextField(null=True, blank=True)
  price = models.IntegerField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def save(self, *args, **kwargs):
    self.book.save()
    super(OverTime, self).save(*args, **kwargs)






class Setting(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
  #  warningn
  paying_warning = models.CharField(max_length=155, null=True, blank=True)
  paying_time_limit = models.IntegerField(null=True, blank=True, default=0)

  # cancel book condition
  cancel_time_limit = models.IntegerField(null=True, blank=True, default=0)

  # total mony
  total_money = models.IntegerField(null=True, default=0)
  waiting_money = models.IntegerField(null=True, default=0)
  cancelled_money = models.IntegerField(null=True, default=0)


  def get_waited_money(self):
    original_total_money_not_paied = Setting.objects.get(id=self.id).waiting_money if self.id else 0
    all_staffs = CustomUser.objects.filter(staff_for=self.user)
    ids=[]
    for i in all_staffs.all():
       ids.append(i.pk)
    if original_total_money_not_paied is not None:
      # not_paied_books = Book.objects.filter((Q(court__user=self.user) | Q(court__user__id__in=ids)) & Q(is_paied=False) & Q(is_cancelled=False))
      not_paied_books = BookTime.objects.filter((Q(book__court__user=self.user) | Q(book__court__user__id__in=ids)) & Q(is_paied=False) & Q(is_cancelled=False))

      current_total_money_not_paied = sum(book.total_price for book in not_paied_books)

      if current_total_money_not_paied != original_total_money_not_paied:
        self.waiting_money = current_total_money_not_paied

  def get_total_money(self):
     # paied
    original_total_money = Setting.objects.get(id=self.id).total_money if self.id else 0
    all_staffs = CustomUser.objects.filter(staff_for=self.user)
    ids=[]
    for i in all_staffs.all():
       ids.append(i.pk)
    if original_total_money is not None:
      paid_books = BookTime.objects.filter((Q(book__court__user=self.user) | Q(book__court__user__id__in=ids)) & Q(is_paied=True) & Q(is_cancelled=False))

      current_total_money = sum(book.total_price for book in paid_books)

      if current_total_money != original_total_money:
        self.total_money = current_total_money

  def get_cancelled_money(self):
    # cancelled
    original_total_money = Setting.objects.get(id=self.id).cancelled_money if self.id else 0
    all_staffs = CustomUser.objects.filter(staff_for=self.user)
    ids=[]
    for i in all_staffs.all():
       ids.append(i.pk)
    if original_total_money is not None:
      c_books = BookTime.objects.filter((Q(book__court__user=self.user) | Q(book__court__user__id__in=ids)) & Q(is_paied=False) & Q(is_cancelled=True))

      current_total_money = sum(book.total_price for book in c_books)

      if current_total_money != original_total_money:
        self.cancelled_money = current_total_money


  def save(self, *args, **kwargs):
    super(Setting, self).save(*args, **kwargs)
    self.get_total_money()
    self.get_waited_money()
    self.get_cancelled_money()
    super(Setting, self).save(*args, **kwargs)

   
class Number(models.Model):
  setting = models.ForeignKey(Setting, on_delete=models.CASCADE, null=True, blank=True)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
  number = models.IntegerField(null=True, blank=True)

  def save(self, *args, **kwargs):
    try:
      self.user = CustomUser.objects.get(phone=self.number)
    except:
      pass
    super(Setting, self).save(*args, **kwargs)




class Notification(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  slot = models.CharField(max_length=100)
  book_time = models.ForeignKey(BookTime, on_delete=models.CASCADE, null=True)
  is_sent = models.BooleanField(default=False, null=True)