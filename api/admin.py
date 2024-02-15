from django.contrib import admin
from . import models


admin.site.register(models.State)

admin.site.register(models.CustomUser)


admin.site.register(models.Court)

admin.site.register(models.BookSetting)
admin.site.register(models.Book)
