from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages, auth

class Index(LoginRequiredMixin, TemplateView):
    template_name = "core/index.html"

class Login(TemplateView):
    template_name = "core/login.html"
    def post(self, *args, **kwargs):
        req = self.request.POST
        usuario = req.get('username')
        senha = req.get('senha')
        user = auth.authenticate(self.request, username=usuario, password=senha)
        if not user:
            messages.add_message(self.request, messages.ERROR,"Usuário ou senha inválidos")
            return render(self.request, self.template_name)
        else:
            auth.login(self.request, user)
            return redirect('index')

def logout(request):
    auth.logout(request)
    return redirect('login')