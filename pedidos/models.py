from django.db import models

# Create your models here.

class Cliente(models.Model):
	tiny_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
	nome = models.CharField(max_length=255)
	email = models.EmailField(blank=True, null=True)
	id_cliente = models.CharField(max_length=100, null=True, blank=True)
	cpf_cnpj = models.CharField(max_length=20, null=True, blank=True)
	telefone = models.CharField(max_length=20, null=True, blank=True)

	def __str__(self):
		return self.nome
	
class Produto(models.Model):
	tiny_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
	nome = models.CharField(max_length=255, null=False, blank=False)
	sku = models.CharField(max_length=100, null=True, blank=True)
	#valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

	def __str__(self):
		return self.nome
	
class Pedido(models.Model):
	tiny_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
	numero = models.CharField(max_length=100, null=True, blank=True)
	data_pedido = models.DateField(null=True, blank=True)
	cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, related_name='pedidos')
	valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	status = models.CharField(max_length=50, null=True, blank=True)

	def __str__(self):
		return f'Pedido {self.numero} - {self.cliente.nome if self.cliente else "Sem Cliente"}'
	
class PedidoItem(models.Model):
	pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
	produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
	quantidade = models.DecimalField(max_digits=12, decimal_places=2, default=1)
	valor_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

	def save(self, *args, **kwargs):
		self.subtotal = (self.quantidade or 0) * (self.valor_unitario or 0)
		super().save(*args, **kwargs)

