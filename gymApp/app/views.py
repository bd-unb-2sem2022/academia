from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import auth
from django.shortcuts import redirect

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from app.models import Unidade, Plano, Modalidade, Aluno, Profissional

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

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(ListView):
    template_name = 'login.html'
    model = Profissional

    def post(self, request, *args, **kwargs):
        cpf = self.request.POST.get('cpf')
        #auth.login(request)
        try:
            Profissional.objects.get(cpf=cpf)
        except:
            return redirect('/login/')
        
        return redirect('/')

    def get_queryset(self):
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    

class CadastroView(TemplateView):
    template_name = 'cadastro.html'

class MontagemTreinoView(LoginRequiredMixin, TemplateView):
    template_name = 'montagem_treino.html'

class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'perfil.html'

class ClienteView(LoginRequiredMixin, TemplateView):
    template_name = 'cliente.html'

