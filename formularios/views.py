from django.shortcuts import render
from django.views.generic import TemplateView


class CadastrodeCliente(TemplateView):
    template_name = "formularios/cadastro_de_clientes.html"