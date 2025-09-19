from django.shortcuts import render
from rest_framework import viewsets
from .models import Cliente, Produto, Pedido
from .serializers import ClienteSerializer, ProdutoSerializer, PedidoSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .services import TinyService

# Create your views here.

class ClienteViewSet(viewsets.ModelViewSet):
	queryset = Cliente.objects.all().order_by('id')
	serializer_class = ProdutoSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
	queryset = Produto.objects.all().order_by('-id')
	serializer_class = ProdutoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
	queryset = Pedido.objects.all().order_by('-data_pedido')
	serializer_class = PedidoSerializer

	#@action(detail=True, methods=['post'])
	#def sincronizar_tiny(self, request, pk=None):
		#pedido = self.get_object()
		#tiny_service = TinyService()
		#result = tiny_service.sincronizar_pedido(pedido)
		#return Response(result)

	@action(detail=False, methods=['post'])
	def sync_from_tiny(sellf, request):
		"""
		Endpoint para disparar sincronização manual dos pedidos do Tiny.
		
		Keyword arguments:
		argument -- description
		Return: return_description
		"""
		tiny = TinyService()
		result = tiny.fetch_pedidos()
		# opicional: retornar resumo do async
		return Response({'status': 'ok', 'imported': result.get('imported', 0)})
	
# opicional: endpoint para disparar sincronização de um pedido específico
# poderia ser action no viewset de pedidos
# class PedidoSyncView(APIView):
#     def post(self, request, pk):
#         try:
#             pedido = Pedido.objects.get(pk=pk)
#         except Pedido.DoesNotExist:
#             return Response({'error': 'Pedido not found'}, status=status.HTTP_404_NOT_FOUND
#         tiny_service = TinyService()
#         result = tiny_service.sincronizar_pedido(pedido)
#         return Response(result)