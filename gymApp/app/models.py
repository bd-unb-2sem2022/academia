from django.db import models


class Unidade(models.Model):
    codigo = models.AutoField(primary_key=True, null=False)
    nome = models.CharField('Nome', max_length=50, null=False)
    endereco = models.CharField('Endereço', max_length=150, null=False)

class Plano(models.Model):
    codigo = models.AutoField(primary_key=True, null=False)
    nome = models.CharField('Nome', max_length=50, null=False)
    valor = models.FloatField('Valor', null=False)

class Modalidade(models.Model):
    codigo = models.AutoField(primary_key=True, null=False)
    nome = models.CharField('Nome', max_length=50, null=False)
    faixa_etaria = models.CharField('Faixa etária', max_length=10, null=False)

class Turma(models.Model):
    codigo = models.AutoField(primary_key=True, null=False)
    fk_modalidade_codigo = models.ForeignKey(Modalidade, on_delete=models.CASCADE, null=False, verbose_name='Modalidade'
    )

class Profissional(models.Model):
    cargo = models.CharField('Cargo', max_length=30, null=False)
    foto = models.BinaryField('Foto')
    cref = models.CharField('CREF', max_length=15, null=False)
    cpf = models.CharField('CPF', max_length=11, unique=True, null=False, primary_key=True)
    nome = models.CharField('Nome', max_length=50, null=False)

class Aluno(models.Model):
    cpf = models.CharField('CPF', max_length=11, unique=True, null=False, primary_key=True)
    nome = models.CharField('Nome', max_length=50, null=False)
    data_nascimento = models.DateField('Data de nascimento', null=False)
    foto = models.BinaryField('Foto')
    fk_plano_codigo = models.ForeignKey(Plano, on_delete=models.CASCADE, null=False, verbose_name='Plano')

class Sala(models.Model):
    codigo = models.AutoField(primary_key=True, null=False)
    numero = models.IntegerField('Número', null=False)
    fk_unidade_codigo = models.ForeignKey(Unidade, on_delete=models.CASCADE, null=False, verbose_name='Unidade')

class Equipamento(models.Model):
    codigo = models.AutoField(primary_key=True, null=False)
    descricao = models.CharField('Descrição', max_length=50, null=False)
    data_aquisicao = models.DateField('Data de nascimento', null=False)
    fk_sala_codigo = models.ForeignKey(Sala, on_delete=models.CASCADE, null=False, verbose_name='Sala')

class Ficha_Treinamento(models.Model):
    codigo = models.AutoField(primary_key=True, null=False)
    vencimento = models.DateField('Vencimento', null=False)
    data_criacao = models.DateField('Data de criação', null=False)
    fk_aluno_cpf  = models.ForeignKey(Aluno, on_delete=models.CASCADE, null=False, verbose_name='Aluno')
    fk_profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, null=False, verbose_name='Profissional')


class Tipo_Exercicio(models.Model):
    codigo = models.AutoField(primary_key=True, null=False)
    nome = models.CharField('Nome', max_length=50, null=False)
    fk_equipamento_codigo = models.ForeignKey(Equipamento, on_delete=models.CASCADE, null=False, verbose_name='Equipamento')

class Exercicio_Prescrito(models.Model):
    num_repeticoes = models.IntegerField('Repetições', null=False)
    num_series = models.IntegerField('Series', null=False)
    tecnica  = models.CharField('Técnica', max_length=50, null=False)
    intervalo_descanso  = models.IntegerField('Intervalo', null=False)
    observacao = models.CharField('Observação', max_length=100, null=False)
    ritmo = models.CharField('Ritmo', max_length=4, null=False)
    codigo = models.AutoField(primary_key=True, null=False)
    fk_tipo_exercicio_codigo = models.ForeignKey(Tipo_Exercicio, on_delete=models.CASCADE, null=False, verbose_name='Exercício')

class E_Composta(models.Model):
    fk_exercicio_prescrito_codigo = models.ForeignKey(Exercicio_Prescrito, on_delete=models.CASCADE, null=False, verbose_name='Exercício prescrito')
    fk_ficha_treinamento_codigo = models.ForeignKey(Ficha_Treinamento, on_delete=models.CASCADE, null=False, verbose_name='Ficha de treinamento')

class Utiliza(models.Model):
    fk_sala_codigo = models.ForeignKey(Sala, on_delete=models.CASCADE, null=False, verbose_name='Sala')
    fk_turma_codigo = models.ForeignKey(Turma, on_delete=models.CASCADE, null=False, verbose_name='Turma')
    horario_inicio = models.TimeField("Início", null=False)
    horario_fim = models.TimeField("Fim", null=False)
    dia_semana = models.CharField("Dias da semana", max_length=10, null=False)

class Conduz(models.Model):
    fk_profissional_cpf = models.ForeignKey(Profissional, on_delete=models.CASCADE, null=False, verbose_name='Profissional')
    fk_turma_codigo = models.ForeignKey(Turma, on_delete=models.CASCADE, null=False, verbose_name='Turma')

class Esta_Matriculado(models.Model):
    fk_turma_codigo = models.ForeignKey(Turma, on_delete=models.CASCADE, null=False, verbose_name='Turma')
    fk_aluno_cpf = models.ForeignKey(Aluno, on_delete=models.CASCADE, null=False, verbose_name='Aluno')

class Da_Acesso(models.Model):
    fk_plano_codigo = models.ForeignKey(Plano, on_delete=models.CASCADE, null=False, verbose_name='Plano')
    fk_unidade_codigo = models.ForeignKey(Unidade, on_delete=models.CASCADE, null=False, verbose_name='Unidade')

class Compreende(models.Model):
    fk_plano_codigo = models.ForeignKey(Plano, on_delete=models.CASCADE, null=False, verbose_name='Plano')
    fk_modalidade_codigo = models.ForeignKey(Modalidade, on_delete=models.CASCADE, null=False, verbose_name='Modalidade')

class Trabalha_Em(models.Model):
    fk_profissional_cpf = models.ForeignKey(Profissional, on_delete=models.CASCADE, null=False, verbose_name='Profissional')
    fk_unidade_codigo = models.ForeignKey(Unidade, on_delete=models.CASCADE, null=False, verbose_name='Unidade')
    horario_inicio = models.TimeField("Início", null=False)
    horario_fim = models.TimeField("Fim", null=False)
    dia_semana = models.CharField("Dias da semana", max_length=10, null=False)
