from django.contrib import admin
from . import models

@admin.register(models.Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['nome', 'classe']


@admin.register(models.Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'documento', 'uf',  "modified", 'created']
    search_fields = ['documento']
    list_filter = ["uf", 'documento', 'tags']
