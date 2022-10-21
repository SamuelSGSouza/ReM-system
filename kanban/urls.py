from django.urls import path
from . import views

urlpatterns = [
    path('', views.Kanban.as_view(), name="kanban"),
    path('kanban_main_content', views.KanbanContent.as_view(), name="kanban_main_content"),
    path('criar_kanban', views.cria_kaban , name="criar_kanban"),
    path('transfere_kanban', views.transfere_kanban , name="transfere_kanban"),
    path('excluir_kanban', views.excluir_kanban , name="excluir_kanban"),
    path('edita_cliente', views.edita_cliente , name="edita_cliente"),
    path('finaliza_cliente', views.finaliza_cliente , name="finaliza_cliente"),
    path('editar_tags', views.editar_tags , name="editar_tags"),
]