from django.urls import path
from . import views

urlpatterns = [
    path('Cadastro de Clientes', views.CadastrodeCliente.as_view(), name="cadastro_cliente")
]