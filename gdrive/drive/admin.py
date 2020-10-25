from django.contrib import admin

from .models import GFile


@admin.register(GFile)
class GFiledmin(admin.ModelAdmin):
    list_display = ["user", "file", "created"]
