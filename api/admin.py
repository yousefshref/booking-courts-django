from django.contrib import admin
from . import models


admin.site.register(models.State)

admin.site.register(models.CustomUser)


admin.site.register(models.Court)
admin.site.register(models.CourtAdditional)
admin.site.register(models.CourtAdditionalTool)

admin.site.register(models.BookSetting)
admin.site.register(models.BookTime)
admin.site.register(models.Book)
