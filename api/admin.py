from django.contrib import admin
from . import models

admin.site.register(models.State)

admin.site.register(models.CustomUser)


class CourtAdmin(admin.ModelAdmin):
  list_display = [field.name for field in models.Court._meta.fields]

  def save_instances(self, request, queryset):
    for i in queryset:
      i.save()

  actions = ['save_instances']

admin.site.register(models.Court,CourtAdmin)
admin.site.register(models.CourtVideo)
admin.site.register(models.CourtImage)
admin.site.register(models.CourtFeature)
admin.site.register(models.CourtType)
admin.site.register(models.CourtTypeT)
admin.site.register(models.CourtAdditional)
admin.site.register(models.CourtAdditionalTool)


admin.site.register(models.Book)
admin.site.register(models.OverTime)
# admin.site.register(models.BookSetting)
admin.site.register(models.BookTime)


admin.site.register(models.Number)
admin.site.register(models.Setting)


admin.site.register(models.Notification)