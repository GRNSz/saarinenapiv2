from rest_framework import serializers
from .models import Cliente, Produto, Pedido, PedidoItem

class ClienteSerializer(serializers.ModelSerializer):
	class Meta: 
		model = Cliente
		fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Produto
		fields = '__all__'

class PedidoItemSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)
    produto_id = serializers.PrimaryKeyRelatedField(queryset=Produto.objects.all(), write_only=True, source='produto')

    class Meta:
        model = PedidoItem
        fields = ['id','produto','produto_id','quantidade','valor_unitario','subtotal']

class PedidoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all(), write_only=True, source='cliente')
    itens = PedidoItemSerializer(many=True, read_only=True)

class Meta:
    model = Pedido
    fields = ['id','tiny_id','numero','data_pedido','cliente','cliente_id','itens','valor_total','lucro_est','status','created_at']	