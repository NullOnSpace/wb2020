from django.contrib import admin

from . import models

# Register your models here.
@admin.register(models.WeiboAccount)
class WeiboAccountAdmin(admin.ModelAdmin):
    pass
