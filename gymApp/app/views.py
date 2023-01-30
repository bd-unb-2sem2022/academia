from django.views.generic import TemplateView

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

class LoginView(TemplateView):
    template_name = 'login.html'

class CadastroView(TemplateView):
    template_name = 'cadastro.html'

class MontagemTreinoView(TemplateView):
    template_name = 'montagem_treino.html'

class PerfilView(TemplateView):
    template_name = 'perfil.html'

class ClienteView(TemplateView):
    template_name = 'cliente.html'
    