from django.contrib import admin
from . import models

@admin.register(models.Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['nome', 'classe']
