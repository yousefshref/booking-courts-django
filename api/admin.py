from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
  list_display = ['id', 'username', 'email', 'phone']
  search_fields = ['username__icontains','phone__icontains', 'email__icontains']

admin.site.register(models.CustomUser, UserAdmin)


# ---------------Court---------------

class CourtImageInline(admin.TabularInline):
    model = models.CourtImage

class CourtVideoInline(admin.TabularInline):
    model = models.CourtVideo
    
class CourtFeaturesInline(admin.TabularInline):
    model = models.CourtFeature


class CourtAdmin(admin.ModelAdmin):
  list_display = ['id', 'user','state', 'title', 'price_per_hour', 'open', 'close', 'is_published']
  list_editable = ['state', 'title', 'price_per_hour', 'open', 'close', 'is_published']

  list_filter = ['state']
  search_fields = ['user__phone__icontains','user__email__icontains', 'user__username__icontains']


  inlines = [
    CourtImageInline,
    CourtVideoInline,
    CourtFeaturesInline,
  ]

  def save_instances(self, request, queryset):
    for i in queryset:
      i.save()

  def publish(self, request, queryset):
    for i in queryset:
      i.is_published = True
      i.save()

  def un_publish(self, request, queryset):
    for i in queryset:
      i.is_published = False
      i.save()

  actions = ['save_instances', 'publish', 'un_publish']

admin.site.register(models.Court,CourtAdmin)


# ---------------TOOLS---------------
class CourtAdditionalToolInline(admin.TabularInline):
    model = models.CourtAdditionalTool

class CourtAdditionalAdmin(admin.ModelAdmin):
  list_display = ['id', 'court__id', 'court__title']
  search_fields = ['court__id', 'court__title__icontains']

  def court__id(req,obj):
    return obj.court.id

  def court__title(req,obj):
    return obj.court.title

  inlines = [CourtAdditionalToolInline]

admin.site.register(models.CourtAdditional, CourtAdditionalAdmin)



admin.site.register(models.CourtType)
admin.site.register(models.CourtTypeT)
admin.site.register(models.State)


# ---------------Book---------------
class OverTimeInline(admin.TabularInline):
    model = models.OverTime

class BookTimeInline(admin.TabularInline):
    model = models.BookTime

from django.utils.html import format_html

class BookAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'court', 'name', 'phone', 'book_date', 'total_price_sum', 'all_books_prices']
  search_fields = ['user__username__icontains', 'user__phone__icontains', 'user__phone__icontains', 'court__title']


  def all_books_prices(req, obj):
    total = 0
    for i in req.get_queryset('c'):
      times = models.BookTime.objects.filter(book__id=i.pk)
      for t in times:
          total += t.total_price
      return format_html('<span style="color: {}; font-size: 30px;">{}</span>', 'green', total)


  def total_price_sum(req, obj):
    total = 0
    times = models.BookTime.objects.filter(book__id=obj.id)
    for i in times.all():
      total += i.total_price
    return total
       
  inlines = [OverTimeInline, BookTimeInline]

admin.site.register(models.Book, BookAdmin)


# ---------------Book---------------
class NumberInline(admin.TabularInline):
    model = models.Number

class SettingAdmin(admin.ModelAdmin):
  inlines = [NumberInline]


admin.site.register(models.Setting, SettingAdmin)

       
# ---------------Not------------
# admin.site.register(models.Notification)