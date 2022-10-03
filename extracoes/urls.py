from django.urls import path
from . import views

urlpatterns = [
    path('Extração de Dados', views.Extracao.as_view(), name="extracao")
]