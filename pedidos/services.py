import os 
import requests 
from django.conf import settings 
from .models import Cliente, Produto, Pedido, PedidoItem
from django.utils.dateparse import parse_datetime
from decimal import Decimal 

TINY_BASE = os.getenv('TINY_API_URL', 'https://api.tiny.com.br/api2/')
TINY_TOKEN = os.getenv('TINY_API_TOKEN', '')

class TinyService:
	def __init__(self, token=None):
		self.base = TINY_BASE.rstrip('/')
		self.token = token or TINY_TOKEN

	def fetch_pedidos(self, pagina=1):
		"""
		
		Chama pedidos.pesquisa.php e importa/atualiza os pedidos no banco.
		Retorna um dicionário com estatísticas.
		
		Keyword arguments:
		argument -- description
		Return: return_description
		"""
		url = f"{self.base}/pedidos.pesquisa.php"
		data = {
			'token': self.token,
			'formato': 'json',
			'pagina': pagina
		}		
		# Tiny aceita POST para pesquisa

		resp = requests.post(url, data=data, timeout=30)
		resp.raise_for_status()
		resp_json = resp.json()

		retorno = resp_json.get('retorno', {})
		pedidos_raw = retorno.get('pedidos', [])
		imported = 0
		for item in pedidos_raw:
			pedido_data = item.get('pedido') or item
			imported += self._save_pedido(pedido_data)

		return {'imported': imported}

def _save_pedido(self, p):
        """
        Recebe um dict representando um pedido do Tiny e salva/atualiza no DB.
        Retorna 1 se importou/atualizou, 0 se ignorado.
        """
        # exemplos de campos usados: id, numero, data_pedido, cliente, itens, valor_total
        tiny_id = str(p.get('id') or p.get('id_pedido') or p.get('numero'))
        numero = p.get('numero') or ''
        data_pedido = p.get('data_pedido')
        # tenta parse; caso falhe, usa agora()
        try:
            dt = parse_datetime(data_pedido) if data_pedido else None
        except Exception:
            from django.utils import timezone
            dt = timezone.now()

        # cliente
        cliente_raw = p.get('cliente') or {}
        cliente_obj = None
        if cliente_raw:
            cliente_tiny_id = cliente_raw.get('id') or cliente_raw.get('codigo') or None
            cliente_obj, _ = Cliente.objects.get_or_create(
                tiny_id=str(cliente_tiny_id) if cliente_tiny_id else None,
                defaults={
                    'nome': cliente_raw.get('nome') or cliente_raw.get('razao_social') or 'Cliente sem nome',
                    'email': cliente_raw.get('email') or None,
                    'telefone': cliente_raw.get('telefone') or None
                }
            )

        # pedido
        pedido, created = Pedido.objects.update_or_create(
            tiny_id=tiny_id,
            defaults={
                'numero': numero,
                'data_pedido': dt or None,
                'cliente': cliente_obj,
                'valor_total': Decimal(str(p.get('valor_total') or p.get('valor_pedido') or 0)),
                'status': p.get('situacao') or p.get('status') or '',
            }
        )

        # itens
        itens_raw = p.get('itens') or []
        # limpa itens antigos (simples) — você pode optar por lógica mais fina
        pedido.itens.all().delete()

        for it in itens_raw:
            descricao = it.get('descricao') or it.get('nome') or 'Produto'
            quantidade = Decimal(str(it.get('quantidade') or it.get('qtde') or 1))
            valor_unitario = Decimal(str(it.get('valor_unitario') or it.get('preco_unitario') or 0))

            # tenta associar produto pelo tiny_id ou nome
            produto_tiny_id = it.get('id_produto') or it.get('produto_id') or None
            produto = None
            if produto_tiny_id:
                produto, _ = Produto.objects.get_or_create(
                    tiny_id=str(produto_tiny_id),
                    defaults={'nome': descricao, 'valor_unitario': valor_unitario}
                )
            else:
                produto, _ = Produto.objects.get_or_create(nome=descricao, defaults={'valor_unitario': valor_unitario})

            PedidoItem.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=quantidade,
                valor_unitario=valor_unitario
            )

        # opcional: calcular lucro estimado (exemplo placeholder)
        # aqui você pode ter uma lógica: custo estimado por produto, etc.
        pedido.lucro_est = pedido.valor_total * Decimal('0.30')  # suposição 30% lucro
        pedido.save()

        return 1	



				