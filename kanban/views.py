from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from . import models
from formularios import models as form_models
from django.contrib import messages
from django.shortcuts import get_object_or_404
from time import time

class Kanban(TemplateView):
    template_name="kanban/kanban.html"
    
    


class KanbanContent(TemplateView):
    template_name = "kanban/kanban_content_main.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        #context para clientes
        qs_clientes = form_models.Cliente.objects.filter(vendedor=self.request.user.username).exclude(kanban="Finalizado")
        context["qtd_clientes"] = qs_clientes.count()
        context['qs_clientes'] = qs_clientes

        #context para kanbans
        qs_kanbans = models.kanbans.objects.filter(vendedor=self.request.user.username)
        context["qtd_kanbans"] = qs_kanbans.count()
        context['qs_kanbans'] = qs_kanbans

        #Usuarios deste vendedor com o kanban inicial Iniciado
        qs_inicial = qs_clientes.filter(kanban="Iniciado")
        context["qtd_inicial"] = qs_inicial.count()
        context['qs_inicial'] = qs_inicial

        #pegando os kanbans deste usuário
        kanbans = list(qs_kanbans.values_list('kanban', flat=True))
        context['kanbans'] = kanbans
        self.request.session['kanbans'] = kanbans
        #Usuarios deste vendedor com o kanban diferente de Iniciado
        qs_clientes_kanbans = qs_clientes.exclude(kanban="Iniciado")
        kanban_clientes = {}
        for kanban in kanbans:
            kanban_cliente = qs_clientes_kanbans.filter(kanban=kanban)
            kanban_clientes[kanban] = kanban_cliente
        context['kanban_clientes'] = kanban_clientes
        


        #TODO: Pegar usuários deste vendedor com kanbans diferentes do inicial

        return context




##################################
######### RETURN JSON ############
##################################
def transfere_kanban(request):
    kanban_destino = request.GET.get('kanban_destino')
    id_cliente = request.GET.get('id_cliente')
    cliente = get_object_or_404(form_models.Cliente, id=id_cliente)
    cliente.kanban = kanban_destino
    cliente.save()
    messages.success(request, f"Cliente Transferido com Sucesso!")
    return JsonResponse({'foo':'bar'})

def cria_kaban(request):
    #TODO: pegar os dados do request
    #cadastrar o novo kaban
    nome_kanban = request.GET.get('nome')
    kanban = models.kanbans.objects.create(vendedor=request.user.username, kanban=nome_kanban)
    kanban.save()
    messages.success(request, f"Kanban Cadastrado Com Sucesso!")

    return JsonResponse({'foo':'bar'})

def edita_cliente(request):
    req = request.GET
    contato_1 = req.get('contato_1')
    contato_2 = req.get('contato_2')
    contato_3 = req.get('contato_3')
    comentario = req.get('comentario')
    id = req.get('id_cliente')
    cliente = get_object_or_404(form_models.Cliente, id=id)
    cliente.contato_1 = contato_1
    cliente.contato_2 = contato_2
    cliente.contato_3 = contato_3
    cliente.comentario = comentario
    cliente.save()
    messages.success(request, f"Cliente Modificado com Sucesso!")
    return JsonResponse({'foo':'bar'})

def finaliza_cliente(request):
    id_cliente = request.GET.get('id_cliente')
    cliente = get_object_or_404(form_models.Cliente, id=id_cliente)
    cliente.kanban = "Finalizado"
    cliente.save()
    messages.success(request, f"Cliente Finalizado Com Sucesso!")
    return JsonResponse({'foo':'bar'})