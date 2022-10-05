from django.urls import path
from . import views

urlpatterns = [
    path('Extração de Dados', views.Extracao.as_view(), name="extracao"),
    path('messages', views.Messages.as_view(), name="messages"),
    path('spinner/spinner', views.Spinner.as_view(), name='spinner'),
    path('baixar_csv', views.csv_download, name='baixar_csv'),
]