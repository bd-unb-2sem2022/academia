from django.contrib import admin

from app.models import Unidade, Plano, Modalidade, Turma, Profissional, Aluno, Sala, Equipamento, Ficha_Treinamento, Tipo_Exercicio, Exercicio_Prescrito, E_Composta, Utiliza, Conduz, Esta_Matriculado, Da_Acesso, Compreende, Trabalha_Em


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('codigo','nome','endereco')

@admin.register(Plano)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('codigo','nome','valor')

@admin.register(Modalidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('codigo','nome','faixa_etaria')

@admin.register(Turma)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('codigo','fk_modalidade_codigo')

@admin.register(Profissional)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('cargo','foto','cref','cpf','nome')

@admin.register(Aluno)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('cpf','nome','data_nascimento','foto','fk_plano_codigo')

@admin.register(Sala)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('codigo','numero','fk_unidade_codigo')

@admin.register(Equipamento)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('codigo','descricao','data_aquisicao','fk_sala_codigo')

@admin.register(Ficha_Treinamento)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('codigo','vencimento','data_criacao','fk_aluno_cpf','fk_profissional')

@admin.register(Tipo_Exercicio)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('codigo','nome','fk_equipamento_codigo')

@admin.register(Exercicio_Prescrito)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('num_repeticoes','num_series','tecnica','intervalo_descanso','observacao','ritmo','codigo','fk_tipo_exercicio_codigo')

@admin.register(E_Composta)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('fk_exercicio_prescrito_codigo','fk_ficha_treinamento_codigo')

@admin.register(Utiliza)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('fk_sala_codigo','fk_turma_codigo','horario_inicio','horario_fim','dia_semana')

@admin.register(Conduz)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('fk_profissional_cpf','fk_turma_codigo')

@admin.register(Esta_Matriculado)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('fk_turma_codigo','fk_aluno_cpf')

@admin.register(Da_Acesso)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('fk_plano_codigo','fk_unidade_codigo')

@admin.register(Compreende)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('fk_plano_codigo','fk_modalidade_codigo')

@admin.register(Trabalha_Em)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('fk_profissional_cpf','fk_unidade_codigo','horario_inicio','horario_fim','dia_semana')

