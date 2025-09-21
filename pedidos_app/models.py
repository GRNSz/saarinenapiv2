from django.db import models
from fornecedores.models import Fornecedor
from transportadoras.models import Transportadora

# Create your models here.

class Cliente(models.Model):
	id_cliente = models.AutoField(primary_key=True)
	
class Pedido(models.Model):
	STATUS_CHOICES = [
		('ABERTO', 'Em Aberto'),
		('FABRICANDO', 'Em Fabricação'),
		('PRONTO', 'Pedido Pronto'),
		('TRANSPORTE', 'Em Transporte'),
		('CONCLUIDO', 'Concluído'),
		('CANCELADO', 'Cancelado'),		
	]

	id_ped = models.AutoField(primary_key=True)
	numero_ped = models.CharField(max_length=100, null=True, blank=True, unique=True)
	cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
	data_pedido = models.DateField(null=True, blank=True)
	fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ABERTO')
	valor_total = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	transportadora = models.ForeignKey(Transportadora, on_delete=models.SET_NULL, null=True, blank=True)
	data_entrega = models.DateField(null=True, blank=True)

	def __str__(self):
		return f'Pedido {self.numero} - {self.cliente}'
	