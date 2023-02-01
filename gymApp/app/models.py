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
