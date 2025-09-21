from django.db import models

# Create your models here.

class Transportadora(models.Model):
	nome = models.CharField(max_length=255, null=False, blank=False)
	email = models.EmailField(blank=True, null=True)
	cnpj = models.CharField(max_length=20, null=True, blank=True)
	telefone = models.CharField(max_length=20, null=True, blank=True)
	endereco = models.CharField(max_length=255, null=True, blank=True)

	def __str__(self):
		return self.nome