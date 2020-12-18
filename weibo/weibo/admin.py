from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.WeiboPost)
admin.site.register(models.WeiboUser)
admin.site.register(models.PostPic)
