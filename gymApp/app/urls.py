
from django.urls import path

from .views import IndexView, LoginView, CadastroView, MontagemTreinoView, PerfilView, ClienteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('montagem_treino/', MontagemTreinoView.as_view(), name='montagem_treino'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('cliente/', ClienteView.as_view(), name='cliente'),
]
