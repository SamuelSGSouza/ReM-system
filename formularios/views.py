from django.shortcuts import render
from django.views.generic import TemplateView

from . import models

class CadastrodeCliente(TemplateView):
    template_name = "formularios/cadastro_de_clientes.html"
    
    def get(self, *args, **kwargs):
        context = {
            'tags': models.Tags.objects.all()
        }
        return render(self.request, self.template_name, context)
    