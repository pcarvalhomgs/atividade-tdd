import pytest
from unittest.mock import MagicMock
from pedido.pedido import Item, Pedido


# =============================================================
# EXEMPLO — um teste pronto, para você copiar o formato
# =============================================================

def test_exemplo_quantidade_total(pedido_pequeno):
    # 1 café + 2 pães de queijo = 3 unidades
    assert pedido_pequeno.quantidade_total() == 3


# =============================================================
# PARTE 1 — Encontre os bugs
# Escreva um teste para cada bug. Cada teste deve FALHAR
# no código original. Não altere src/pedido/pedido.py ainda.
# =============================================================



# =============================================================
# PARTE 2 — Implemente com TDD
# Siga o ciclo: 🔴 escreva o teste → 🟢 implemente → 🟡 refatore
# =============================================================

# Requisito 1 — contar_frete_gratis(pedidos) -> int
# Escreva os testes ANTES de implementar a função



# Requisito 2 — situacao(unidades_indisponiveis) -> str
# Escreva os testes ANTES de implementar o método



# Requisito 3 — sugerir_frete_gratis(sms_service) -> None
# Use MagicMock para simular o serviço de SMS
# Escreva os testes ANTES de implementar o método

def test_bug_1_subtotal_considera_quantidades(pedido_pequeno):
    # 6 * 1 + 4,50 * 2 = 15; somar apenas os preços daria 10,50.
    assert pedido_pequeno.subtotal() == pytest.approx(15.0)

def test_bug_2_frete_gratis_inclui_cinquenta_reais():
    pedido = Pedido("Carla", [Item("Combo", 50.0)])
    assert pedido.tem_frete_gratis() is True

def test_bug_3_item_mais_barato_usa_menor_preco(pedido_pequeno):
    # O pão custa 4,50 por unidade, mesmo tendo duas unidades no pedido.
    assert pedido_pequeno.item_mais_barato() == Item("Pão de queijo", 4.5, 2)

def test_bug_4_desconto_reduz_o_subtotal():
    # Quantidade 1 isola o desconto do bug no cálculo do subtotal.
    pedido = Pedido("Carla", [Item("Combo", 100.0)])
    assert pedido.total_com_desconto(10) == pytest.approx(90.0)
