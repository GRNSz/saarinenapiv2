from django.contrib import admin
from .models import Cliente, Produto, Pedido, PedidoItem


# Register your models here.

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
	list_display = ('nome', 'email', 'telefone', 'tiny_id')
	search_fields = ('nome', 'email', 'tiny_id')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
	list_display = ('id', 'nome', 'sku', 'valor_unitario', 'tiny_id')
	search_fields = ('nome', 'sku', 'tiny_id')

class PedidoItemInline(admin.TabularInline):
	model = PedidoItem
	extra = 0

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
	list_display = ('id', 'numero', 'cliente', 'data_pedido', 'valor_total', 'status')
	inlines = [PedidoItemInline]
	#search_fields = ('numero', 'cliente__nome', 'tiny_id')
	#list_filter = ('status', 'data_pedido')
	#ordering = ('-data_pedido',)	

