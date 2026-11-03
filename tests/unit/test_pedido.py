import pytest
from unittest.mock import MagicMock

from pedido.pedido import Item, Pedido, contar_frete_gratis


def test_exemplo_quantidade_total(pedido_pequeno):
    # 1 café + 2 pães de queijo = 3 unidades.
    assert pedido_pequeno.quantidade_total() == 3


# Parte 1: regressões dos quatro bugs encontrados.
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

# Cada linha parametrizada é executada como um caso independente.
@pytest.mark.parametrize(
    "subtotais, esperado",
    [
        pytest.param([50.0, 73.0], 2, id="todos-com-frete-gratis"),
        pytest.param([15.0, 49.99], 0, id="nenhum-com-frete-gratis"),
        pytest.param([15.0, 50.0, 73.0], 2, id="lista-mista"),
        pytest.param([], 0, id="lista-vazia"),
    ],
)
def test_contar_frete_gratis(subtotais, esperado):
    pedidos = [Pedido("Cliente", [Item("Combo", valor)]) for valor in subtotais]
    assert contar_frete_gratis(pedidos) == esperado

# Cada linha parametrizada é executada como um caso independente.
@pytest.mark.parametrize(
    "preco, quantidade, indisponiveis, esperado",
    [
        pytest.param(20.0, 4, 2, "Cancelado por falta de estoque",
                     id="estoque-tem-prioridade-sobre-frete"),
        pytest.param(12.5, 4, 0, "Confirmado com frete grátis",
                     id="tudo-disponivel-com-frete"),
        pytest.param(10.0, 4, 0, "Confirmado",
                     id="tudo-disponivel-sem-frete"),
        pytest.param(20.0, 4, 1, "Confirmado com frete grátis",
                     id="exatos-25-por-cento-com-frete"),
        pytest.param(10.0, 4, 1, "Confirmado",
                     id="exatos-25-por-cento-sem-frete"),
        pytest.param(1.0, 100, 26, "Cancelado por falta de estoque",
                     id="26-por-cento-cancela"),
    ],
)
def test_situacao_respeita_estoque_e_frete(preco, quantidade, indisponiveis, esperado):
    # 1/4 = 25%; 26/100 = 26%, pouco acima do limite.
    pedido = Pedido("Carla", [Item("Lanche", preco, quantidade)])
    assert pedido.situacao(indisponiveis) == esperado

def test_sugerir_frete_gratis_envia_cliente_e_valor_faltante(pedido_pequeno):
    sms_service = MagicMock()
    pedido_pequeno.sugerir_frete_gratis(sms_service)
    # O mock registra a chamada sem enviar um SMS real.
    sms_service.enviar.assert_called_once_with("Bruno", 35.0)


# Cada linha parametrizada é executada como um caso independente.
@pytest.mark.parametrize("subtotal", [73.0, 50.0], ids=["acima-do-limite", "no-limite"])
def test_sugerir_frete_gratis_nao_aciona_servico_quando_tem_frete(subtotal):
    sms_service = MagicMock()
    pedido = Pedido("Ana", [Item("Combo", subtotal)])
    pedido.sugerir_frete_gratis(sms_service)
    sms_service.enviar.assert_not_called()
    assert sms_service.mock_calls == []


def test_sugerir_frete_gratis_arredonda_valor_para_centavos():
    sms_service = MagicMock()
    pedido = Pedido("Carla", [Item("Suco", 8.1)])
    pedido.sugerir_frete_gratis(sms_service)
    # Evita passar 41.900000000000006 ao serviço.
    sms_service.enviar.assert_called_once_with("Carla", 41.9)
