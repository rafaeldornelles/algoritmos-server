from django.db import models

# Create your models here.

class Bairro(models.Model):
    descricao = models.CharField(max_length=200)

class Locais(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.CharField(max_length=300)

class Paciente(models.Model):
    nome = models.CharField(max_length=200)
    bairro = models.ForeignKey(Bairro, on_delete=models.PROTECT)
    locaisVisitados = models.ManyToManyField(Locais, null=True, blank=True)

class FormaContagio(models.Model):
    descricao = models.CharField(max_length=200)

class Sintoma(models.Model):
    descricao = models.CharField(max_length=200)

class Caso(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    formaContagio = models.ForeignKey(FormaContagio, on_delete=models.PROTECT)
    dataInicioSintomas = models.DateTimeField()
    dataRelato = models.DateTimeField()
    dataFimSintomas = models.DateTimeField(null=True, blank=True)
    sintomas = models.ManyToManyField(Sintoma)
