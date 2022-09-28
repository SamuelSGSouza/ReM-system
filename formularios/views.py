from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages

from . import models
from . import forms

class CadastrodeCliente(TemplateView):
    template_name = "formularios/cadastro_de_clientes.html"
    
    def get(self, *args, **kwargs):
        context = {
            'tags': models.Tags.objects.all(),
            'form': forms.ClienteForm()
        }
        return render(self.request, self.template_name, context)
    def post(self, *args, **kwargs):
        req = self.request.POST
        form = forms.ClienteForm(req)
        context = {
            'tags': models.Tags.objects.all(),
        }
        if form.is_valid():
            messages.success(self.request, "Cadastro realizado com sucesso")
        else:  
            messages.error(self.request, f"Cadastro teve um erro")
            dicionario = {k: v[0] if len(v) == 1 else v for k, v in req.lists()}
            context['dict'] = dicionario
            context['form'] = form
        return render(self.request, self.template_name, context)