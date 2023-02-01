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
    fk_modalidade_codigo = models.ForeignKey(Modalidade, on_delete=models.CASCADE, default=Modalidade, null=False, verbose_name='Modalidade')

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
    fk_plano_codigo = models.ForeignKey(Plano, on_delete=models.CASCADE, default=Plano, null=False, verbose_name='Plano')

class Sala(models.Model):
    codigo = models.AutoField(primary_key=True, null=False)
    numero = models.IntegerField('Número', null=False)
    fk_unidade_codigo = models.ForeignKey(Unidade, on_delete=models.CASCADE, default=Unidade, null=False, verbose_name='Unidade')

class Equipamento(models.Model):
    codigo = models.AutoField(primary_key=True, null=False)
    descricao = models.CharField('Descrição', max_length=50, null=False)
    data_aquisicao = models.DateField('Data de nascimento', null=False)
    fk_sala_codigo = models.ForeignKey(Sala, on_delete=models.CASCADE, default=Sala, null=False, verbose_name='Sala')

class FichaTreinamento(models.Model):
    codigo = models.AutoField(primary_key=True, null=False)
    vencimento = models.DateField('Vencimento', null=False)
    data_criacao = models.DateField('Data de criação', null=False)
    fk_aluno_cpf  = models.ForeignKey(Aluno, on_delete=models.CASCADE, default=Aluno, null=False, verbose_name='Aluno')
    fk_profissional = models.ForeignKey(Profissional, default=Profissional, on_delete=models.CASCADE, null=False, verbose_name='Profissional')


class TipoExercicio(models.Model):
    codigo = models.AutoField(primary_key=True, null=False)
    nome = models.CharField('Nome', max_length=50, null=False)
    fk_equipamento_codigo = models.ForeignKey(Equipamento, default=Equipamento, on_delete=models.CASCADE, null=False, verbose_name='Equipamento')

class ExercicioPrescrito(models.Model):
    num_repeticoes = models.IntegerField('Repetições', null=False)
    num_series = models.IntegerField('Series', null=False)
    tecnica  = models.CharField('Técnica', max_length=50, null=False)
    intervalo_descanso  = models.IntegerField('Intervalo', null=False)
    observacao = models.CharField('Observação', max_length=100, null=False)
    ritmo = models.CharField('Ritmo', max_length=4, null=False)
    codigo = models.AutoField(primary_key=True, null=False)
    fk_tipo_exercicio_codigo = models.ForeignKey(TipoExercicio, default=TipoExercicio, on_delete=models.CASCADE, null=False, verbose_name='Exercício')

