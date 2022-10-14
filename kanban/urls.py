from django.urls import path
from . import views

urlpatterns = [
    path('', views.Kanban.as_view(), name="kanban"),
    path('kanban_main_content', views.KanbanContent.as_view(), name="kanban_main_content"),
    path('criar_kanban', views.cria_kaban , name="criar_kanban"),
    path('transfere_kanban', views.transfere_kanban , name="transfere_kanban"),
    path('edita_cliente', views.edita_cliente , name="edita_cliente"),
    path('finaliza_cliente', views.finaliza_cliente , name="finaliza_cliente"),
]