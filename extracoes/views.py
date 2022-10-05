from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib import messages
from formularios import models as form_models
from django.contrib.messages import get_messages

from . import threading
from . import functions

from datetime import datetime
import os

from django.conf import settings #TODO: remover esta linha
class Extracao(LoginRequiredMixin, ListView):
    model = form_models.Cliente
    context_object_name = 'qs'
    paginate_by = 10
    ordering = "documento"
    template_name = "extracao/extracao.html"

    def get_queryset(self):
        #pegando o request e transformando em dicionário
        filtros = {k: v[0] if len(v) == 1 else v for k, v in self.request.GET.lists()}
        print(filtros)
        qs = super().get_queryset()
        try: #verificando se a thread foi encontrada

            if thread.is_alive():#se a thread estiver ativa, pegar apenas 1 valor
                qs = functions.filtra_qs(self.model, filtros)
                qs = qs.order_by('documento')[:1]
            else: #se a thread não estiver ativa, pegar todo o queryset
                qs = functions.filtra_qs(self.model, filtros)
                qs = qs.order_by('documento')

        except:# se a thread não foi encontrada, trazer todo o queryset
            qs = functions.filtra_qs(self.model, filtros)
            qs = qs.order_by('documento')

        self.request.session['filtros'] = filtros
        return qs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = form_models.Tags.objects.all()
        context['teste'] = settings.MEDIA_ROOT #TODO: remover esta linha
        return context

    def post(self, *args, **kwargs):
        #definindo o queryset a partir da função de filtros
        filtros = self.request.session['filtros']
        qs = functions.filtra_qs(self.model, filtros)

        #criando a thread que irá gerar o csv
        global thread 
        thread = threading.ThreadGerarCsv(self.request,functions.gera_csv,qs)
        thread.start()

        #criando as messages que informam o início da thread
        self.request.session['cadastrando'] = "True"
        messages.success(self.request, "O Csv está sendo gerado")

        return render(self.request, self.template_name)

class Messages(LoginRequiredMixin,TemplateView):
    template_name = 'parcials/_alerts.html'
    def get(self, *args, **kwargs):
        context = {}
        context['cadastrando'] = "True"
        try:
            #verificando se a thread acabou de rodar
            if thread.is_alive():
                messages.info(self.request, f"Threading ainda acontecendo")

            else:
                context['cadastrando'] = "False"
                context['cadastro_finalizado'] = 'True'
                self.request.session['path'] = thread.path
                try:
                    del self.request.session['cadastrando']
                except:
                    pass
                messages.success(self.request, "Threading Finalizada com Sucesso")

        except NameError:
            try:
                del self.request.session['cadastrando']
            except:
                pass
            context['cadastrando'] = "False"
            messages.error(self.request, f"O subprocesso foi interrompido pelo servidor. Por favor tente novamente.")
        
        except Exception as e:
            try:
                del self.request.session['cadastrando']
            except:
                pass
            context['cadastrando'] = "False"
            messages.error(self.request, f"Erro do tipo {type(e)}. Erro {e}.")

        storage = get_messages(self.request)
        if len(storage) < 1 and self.request.session['cadastrando'] == "True": 
            messages.info(self.request, f'Dados Sendo Cadastrados. Não feche ou recarregue esta página.')
        try:
            print(self.request.session["teste"])
        except:
            pass 
        return render(self.request, self.template_name, context)

class Spinner(TemplateView):
    template_name = 'parcials/_spinner.html'
    def get(self, *args, **kwargs): 
        return render(self.request, self.template_name)

def csv_download(request):
    csv = open(request.session['path'], 'rb')
    response = HttpResponse(csv, content_type='text/csv')
    os.remove(request.session['path'])
    hoje = datetime.today()
    response['Content-Disposition'] = f"attachment; filename=Extracao_{request.user.username}_{hoje}.csv"
    return response