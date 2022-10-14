from django.contrib import admin
from . import models

@admin.register(models.kanbans)
class kanbansAdmin(admin.ModelAdmin):
    list_display = ['vendedor', 'kanban', 'created', 'modified']
    search_fields = ['vendedor', 'kanban', 'modified']
    list_filter = ['vendedor', 'kanban', 'modified']
