from django.contrib import admin

from app.models import Unidade, Plano, Modalidade


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'endereco')

@admin.register(Plano)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'valor')

@admin.register(Modalidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'faixa_etaria')


