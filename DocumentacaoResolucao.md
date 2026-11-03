# Descobertas, correções e implementações

## Descoberta e correção dos quatro bugs

Antes das correções, foram escritos quatro testes que demonstraram os erros.
O código de produção só foi alterado depois que os quatro testes falharam.

### 1. Subtotal ignorava as quantidades

O método somava apenas o preço unitário de cada tipo de item. Um café de
R$ 6,00 e dois pães de queijo de R$ 4,50 resultavam em R$ 10,50.
O resultado correto é R$ 15,00: `6 × 1 + 4,50 × 2`.

A correção em `subtotal()` multiplica o preço pela quantidade antes de somar:

```python
return sum(item.preco * item.quantidade for item in self.itens)
```

### 2. Frete grátis excluía exatamente R$ 50,00

A comparação usava `>`, portanto um pedido de exatamente R$ 50,00 não tinha
frete grátis. O teste desse valor revelou o erro de fronteira.
A correção usa `>= VALOR_FRETE_GRATIS`, incluindo o limite.

### 3. Item mais barato retornava o maior preço

O método `item_mais_barato()` usava `max`, retornando o café de R$ 6,00 em vez
do pão de queijo de R$ 4,50. A correção substitui `max` por `min`, mantendo o
preço unitário como critério, independentemente da quantidade comprada.

### 4. Desconto aumentava o total

O método somava o desconto ao subtotal. Com R$ 100,00 e desconto de 10%,
retornava R$ 110,00. O teste usa quantidade 1 para isolar esse problema do erro
no subtotal. A correção subtrai o desconto e retorna R$ 90,00:

```python
subtotal = self.subtotal()
return subtotal - subtotal * percentual / 100
```

Após cada correção, os testes foram executados novamente. A quantidade de
falhas caiu de quatro para zero, resultando em cinco testes passando,
incluindo o exemplo original.

## Implementação dos requisitos com TDD

Cada requisito começou com testes falhando (Red), seguido da implementação
que os fez passar (Green). Depois, o código foi refatorado sem alterar os
comportamentos verificados pelos testes.

### 1. Contagem de pedidos com frete grátis

A função `contar_frete_gratis(pedidos)` reutiliza `tem_frete_gratis()` para
contar os pedidos elegíveis:

```python
return sum(1 for pedido in pedidos if pedido.tem_frete_gratis())
```

Os testes cobrem todos os pedidos com frete grátis, nenhum elegível, uma lista
mista e uma lista vazia. Primeiro falharam porque a função não existia;
com uma função vazia, falharam porque o retorno era `None`. Após implementar
a contagem, os nove testes existentes passaram. A lista vazia retorna zero.

### 2. Situação do pedido considerando estoque

O método `situacao(unidades_indisponiveis)` calcula a proporção entre unidades
indisponíveis e quantidade total. A avaliação respeita esta ordem:

1. Mais de 25% indisponível: `"Cancelado por falta de estoque"`.
2. Caso contrário, pedido com frete grátis: `"Confirmado com frete grátis"`.
3. Nos demais casos: `"Confirmado"`.

O cancelamento tem prioridade mesmo quando o pedido possui frete grátis.
Exatamente 25% não cancela: um pedido com quatro unidades e uma indisponível
continua para a avaliação do frete. Com 26 de 100 unidades indisponíveis,
o pedido é cancelado.

Os seis testes cobrem a prioridade do estoque, disponibilidade total com e sem
frete, exatamente 25% com e sem frete e 26% indisponível. Antes da implementação,
falharam por ausência do método; depois, os 15 testes existentes passaram.
O método pressupõe quantidade total positiva, pois o enunciado não define
uma situação para pedidos com zero unidades.

### 3. Sugestão de frete grátis por SMS

O método `sugerir_frete_gratis(sms_service)` recebe o serviço por parâmetro.
Se o pedido ainda não tem frete grátis, calcula quanto falta e chama
`sms_service.enviar(cliente, valor_faltante)`.

Nos testes, `MagicMock` substitui o serviço externo e registra as chamadas,
sem enviar SMS reais. Para Bruno, cujo subtotal é R$ 15,00, o teste exige
exatamente uma chamada `enviar("Bruno", 35.0)`.

Pedidos de exatamente R$ 50,00 ou acima desse valor não acionam o serviço.
Um teste adicional verifica subtotal de R$ 8,10 e valor faltante de R$ 41,90.
A implementação usa `round(..., 2)` para evitar resíduos de ponto flutuante
no valor enviado ao serviço.

Os quatro testes falharam inicialmente por ausência do método e passaram
após a implementação, totalizando 19 testes passando.

## Refatoração das implementações

A constante `LIMITE_INDISPONIBILIDADE = 0.25` dá nome à regra de estoque.
O desconto calcula o subtotal uma única vez. Comentários explicam os limites
de R$ 50,00 e 25%, a substituição do serviço por Mock e o arredondamento.
Os testes parametrizados executam cada cenário como um caso independente.

A validação final reuniu o exemplo original, quatro testes de regressão e
14 casos dos novos requisitos: os 12 obrigatórios e dois adicionais.
