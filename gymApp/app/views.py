from django.views.generic import TemplateView, ListView

from app.models import Unidade, Plano, Modalidade

# Create your views here.

class IndexView(ListView):
    template_name = 'index.html'
    
    model = Unidade
    context_object_name = 'unidades'

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        context['planos'] = Plano.objects.all()
        context['modalidades'] = Modalidade.objects.all()

        return context

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
    