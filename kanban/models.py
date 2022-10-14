from django.db import models
from model_utils.models import TimeStampedModel

class kanbans(TimeStampedModel):
    class Meta:
        verbose_name_plural = "Kanban"
    vendedor = models.CharField(max_length=255, verbose_name="Vendedor")
    kanban = models.CharField(max_length=255, verbose_name="Nome do Kanban")

