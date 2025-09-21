from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Q
from .models import Pedido  # Corrigido: era pedidos_app
from rest_framework import viewsets
from .serializers import ClienteSerializer, ProdutoSerializer, PedidoSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .services import TinyService

def listar_pedidos(request):
    pedidos = Pedido.objects.all().values()  # Corrigido: era pedidos_app
    return JsonResponse(list(pedidos), safe=False)

def status_dashboard(request):
    # Versão otimizada com uma única query
    stats = Pedido.objects.aggregate(  # Corrigido: era pedidos_app
        total=Count('id'),
        abertos=Count('id', filter=Q(status='ABERTO')),
        fabricando=Count('id', filter=Q(status='FABRICANDO')),
        transporte=Count('id', filter=Q(status='TRANSPORTE')),
        concluidos=Count('id', filter=Q(status='CONCLUIDO')),
        cancelados=Count('id', filter=Q(status='CANCELADO'))
    )
    
    return JsonResponse(stats)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('id')
    serializer_class = ClienteSerializer  # Corrigido: era ProdutoSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all().order_by('-id')
    serializer_class = ProdutoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by('-data_pedido')
    serializer_class = PedidoSerializer

    @action(detail=False, methods=['post'])
    def sync_from_tiny(self, request):
        """
        Endpoint para disparar sincronização manual dos pedidos do Tiny.
        """
        tiny = TinyService()
        result = tiny.fetch_pedidos()
        return Response({'status': 'ok', 'imported': result.get('imported', 0)})