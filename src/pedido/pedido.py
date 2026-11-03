from dataclasses import dataclass

VALOR_FRETE_GRATIS = 50.0
LIMITE_INDISPONIBILIDADE = 0.25


@dataclass
class Item:
    nome: str
    preco: float
    quantidade: int = 1


class Pedido:
    def __init__(self, cliente: str, itens: list):
        self.cliente = cliente
        self.itens = itens

    def quantidade_total(self) -> int:
        return sum(item.quantidade for item in self.itens)

    def subtotal(self) -> float:
        # Cada unidade contribui para o valor, não apenas cada tipo de item.
        return sum(item.preco * item.quantidade for item in self.itens)

    def tem_frete_gratis(self) -> bool:
        # O limite é inclusivo: exatamente R$ 50 também dá frete grátis.
        return self.subtotal() >= VALOR_FRETE_GRATIS

    def item_mais_caro(self) -> Item:
        return max(self.itens, key=lambda item: item.preco)

    def item_mais_barato(self) -> Item:
        return min(self.itens, key=lambda item: item.preco)

    def total_com_desconto(self, percentual: float) -> float:
        subtotal = self.subtotal()
        return subtotal - subtotal * percentual / 100

    def situacao(self, unidades_indisponiveis: int) -> str:
        """Avalia o estoque de um pedido com quantidade total positiva."""
        # O cancelamento tem prioridade; exatamente 25% ainda permite confirmar.
        percentual_indisponivel = unidades_indisponiveis / self.quantidade_total()
        if percentual_indisponivel > LIMITE_INDISPONIBILIDADE:
            return "Cancelado por falta de estoque"
        if self.tem_frete_gratis():
            return "Confirmado com frete grátis"
        return "Confirmado"

    def sugerir_frete_gratis(self, sms_service) -> None:
        # Receber o serviço permite substituí-lo por um Mock durante os testes.
        if not self.tem_frete_gratis():
            # A diferença deve ser enviada em reais e centavos.
            valor_faltante = round(VALOR_FRETE_GRATIS - self.subtotal(), 2)
            sms_service.enviar(self.cliente, valor_faltante)


def contar_frete_gratis(pedidos: list) -> int:
    """Reutiliza a regra de frete de cada pedido; lista vazia resulta em zero."""
    return sum(1 for pedido in pedidos if pedido.tem_frete_gratis())
