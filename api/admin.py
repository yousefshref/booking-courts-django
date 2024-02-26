from django.contrib import admin
from . import models


admin.site.register(models.State)

admin.site.register(models.CustomUser)


admin.site.register(models.Court)
admin.site.register(models.CourtVideo)
admin.site.register(models.CourtImage)
admin.site.register(models.CourtFeature)
admin.site.register(models.CourtType)
admin.site.register(models.CourtTypeT)
admin.site.register(models.CourtAdditional)
admin.site.register(models.CourtAdditionalTool)


admin.site.register(models.Book)
admin.site.register(models.OverTime)
admin.site.register(models.BookSetting)
admin.site.register(models.BookTime)