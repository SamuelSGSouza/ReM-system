from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from formularios import models as form_models

class Extracao(LoginRequiredMixin, ListView):
    model = form_models.Cliente
    context_object_name = 'qs'
    paginate_by = 10
    ordering = "documento"
    template_name = "extracao/extracao.html"
