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
    
    def get_context_data(self, **kwargs):

        #context para kanbans
        qs_kanbans = models.kanbans.objects.filter(vendedor=self.request.user.username).order_by("id")
        self.request.session["qtd_kanbans"] = int(qs_kanbans.count())
        # self.request.session['qs_kanbans'] = list(qs_kanbans.values())
        self.request.session['kanbans'] = list(qs_kanbans.values_list('kanban', flat=True))

        #context para clientes
        qs_clientes = form_models.Cliente.objects.filter(vendedor=self.request.user.username).exclude(kanban="Finalizado").order_by("id")
        clientes = list(qs_clientes.values_list("id", "nome", "documento", "contato_1","contato_2","contato_3", "comentario", "kanban"))
        print(clientes)
        #transformando clientes numa lista de dicts
        cli = []
        for cliente in clientes:
            cl = {}
            cl["id"] = cliente[0]
            cl["nome"] = cliente[1]
            cl["documento"] = cliente[2]
            cl["contato_1"] = cliente[3]
            cl["contato_2"] = cliente[4]
            cl["contato_3"] = cliente[5]
            cl["comentario"] = cliente[6]
            cl["kanban"] = cliente[7]
            cl["tags"] = list(form_models.Cliente.objects.get(id=cliente[0]).tags.all().values())
            cli.append(cl)
        
        print(len(cli))
        #passando os resultados para a session
        self.request.session['qs_clientes'] = cli
        self.request.session["qtd_clientes"] = int(qs_clientes.count())

        return super().get_context_data(**kwargs)


class KanbanContent(TemplateView):
    template_name = "kanban/kanban_content_main.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        #pegar todos os clientes da sessao

        #context para clientes
        qs_clientes = self.request.session['qs_clientes']
        context["qtd_clientes"] = self.request.session["qtd_clientes"]
        #separando clientes em inical e não inicial
        qs_inicial = []
        qs_clientes_geral = []
        for cliente in qs_clientes:
            if cliente['kanban'] == "Iniciado":
                qs_inicial.append(cliente)
            elif cliente['kanban'] != "Finalizado":
                qs_clientes_geral.append(cliente)

        #Usuarios deste vendedor com o kanban inicial Iniciadol
        context["qtd_inicial"] = len(qs_inicial)
        context['qs_inicial'] = qs_inicial

        #pegando os kanbans deste usuário
        kanbans = self.request.session["kanbans"]
        context['kanbans'] = kanbans

        #Usuarios deste vendedor com o kanban diferente de Iniciado
        kanban_clientes = {}
        for kanban in self.request.session['kanbans']:
            lista = []
            for cliente in qs_clientes_geral:
                if cliente['kanban'] ==kanban:
                    lista.append(cliente)
            kanban_clientes[kanban] = lista
        context['kanban_clientes'] = kanban_clientes
        


        #TODO: Pegar usuários deste vendedor com kanbans diferentes do inicial

        return context

##################################
######### RETURN JSON ############
##################################
def transfere_kanban(request):
    kanban_destino = request.GET.get('kanban_destino')
    id_cliente = int(request.GET.get('id_cliente'))
    cliente = get_object_or_404(form_models.Cliente, id=id_cliente)
    cliente.kanban = kanban_destino
    cliente.save()

    clientes = request.session['qs_clientes']
    for cliente in clientes:
        if int(cliente['id']) == id_cliente:
            cliente['kanban'] = kanban_destino
            break
    request.session['qs_clientes'] = clientes

    messages.success(request, f"Cliente Transferido com Sucesso!")
    return JsonResponse({'foo':'bar'})

def cria_kaban(request):
    #cadastrar o novo kaban
    nome_kanban = request.GET.get('nome')
    kanban = models.kanbans.objects.create(vendedor=request.user.username, kanban=nome_kanban)
    kanban.save()

    #atualizando sessao
    request.session["qtd_kanbans"] = int(request.session["qtd_kanbans"] + 1)
    lista = request.session['kanbans']
    lista.append(nome_kanban)
    request.session['kanbans'] = lista

    #enviando mensagem
    messages.success(request, f"Kanban Cadastrado Com Sucesso!")

    return JsonResponse({'foo':'bar'})

def edita_cliente(request):
    req = request.GET
    contato_1 = req.get('contato_1')
    contato_2 = req.get('contato_2')
    contato_3 = req.get('contato_3')
    comentario = req.get('comentario')
    id = int(req.get('id_cliente'))
    cliente = get_object_or_404(form_models.Cliente, id=id)
    cliente.contato_1 = contato_1
    cliente.contato_2 = contato_2
    cliente.contato_3 = contato_3
    cliente.comentario = comentario
    cliente.save()

    clientes = request.session['qs_clientes']
    for cliente in clientes:
        if int(cliente['id']) == id:
            cliente['contato_1'] = contato_1
            cliente['contato_2'] = contato_2
            cliente['contato_3'] = contato_3
            cliente['comentario'] = comentario
            break
    request.session['qs_clientes'] = clientes
    messages.success(request, f"Cliente Modificado com Sucesso!")
    return JsonResponse({'foo':'bar'})

def finaliza_cliente(request):
    id_cliente = int(request.GET.get('id_cliente'))
    cliente = get_object_or_404(form_models.Cliente, id=id_cliente)
    cliente.kanban = "Finalizado"
    cliente.save()

    clientes = request.session['qs_clientes']
    for cliente in clientes:
        if int(cliente['id']) == id_cliente:
            cliente['kanban'] = "Finalizado"
            break
    request.session['qs_clientes'] = clientes
    messages.success(request, f"Cliente Finalizado Com Sucesso!")
    return JsonResponse({'foo':'bar'})